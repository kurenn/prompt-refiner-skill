#!/usr/bin/env python3
"""Benchmark runner for the prompt-refiner skill.

Usage:
    python evals/run_evals.py --skill-path SKILL.md --label baseline
    python evals/run_evals.py --skill-path SKILL.md --label improved
    python evals/run_evals.py --compare results/run_baseline.json results/run_improved.json
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime
from importlib import import_module
from pathlib import Path

import anthropic

# Ensure evals package is importable
sys.path.insert(0, str(Path(__file__).parent))
import config

from assertions.structural import ASSERTIONS as STRUCTURAL
from assertions.mode_compliance import ASSERTIONS as MODE
from assertions.proportionality import ASSERTIONS as PROPORTIONALITY

ALL_ASSERTIONS = {**STRUCTURAL, **MODE, **PROPORTIONALITY}

JUDGE_MODULES = {
    "expansion_quality": "judges.expansion_quality",
    "actionability": "judges.actionability",
    "consumability": "judges.consumability",
}


def load_skill(skill_path: str) -> str:
    with open(skill_path) as f:
        return f.read()


def load_scenarios(scenarios_dir: str) -> list[dict]:
    scenarios = []
    for path in sorted(Path(scenarios_dir).glob("*.json")):
        with open(path) as f:
            scenarios.append(json.load(f))
    return scenarios


def build_messages(scenario: dict) -> list[list[dict]]:
    """Build conversation turns for a scenario.

    Returns a list of turns, where each turn is a list of messages to send.
    For one-shot: single turn with the user request.
    For interactive/hybrid: first turn is the request, second turn has mock answers.
    """
    mode = scenario["mode"]
    mode_instruction = {
        "one-shot": "Use One-Shot mode.",
        "interactive": "Use Interactive mode.",
        "hybrid": "Use Hybrid mode.",
    }[mode]

    first_message = f"{scenario['input']}\n\n{mode_instruction}"
    turns = [[{"role": "user", "content": first_message}]]

    if scenario.get("mock_answers") and mode in ("interactive", "hybrid"):
        turns.append([{"role": "user", "content": scenario["mock_answers"]}])

    return turns


def run_conversation(client: anthropic.Anthropic, skill_content: str,
                     turns: list[list[dict]]) -> str:
    """Run a multi-turn conversation, return the final assistant output."""
    messages = []
    final_output = ""

    for turn in turns:
        messages.extend(turn)
        response = client.messages.create(
            model=config.MODEL,
            max_tokens=config.MAX_TOKENS,
            temperature=config.TEMPERATURE,
            system=[
                {
                    "type": "text",
                    "text": skill_content,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=messages,
        )
        assistant_text = response.content[0].text
        messages.append({"role": "assistant", "content": assistant_text})
        final_output = assistant_text

    # For multi-turn, concatenate all assistant responses for evaluation
    all_assistant = "\n\n---\n\n".join(
        m["content"] for m in messages if m["role"] == "assistant"
    )
    return all_assistant


def run_assertions(output: str, scenario: dict) -> dict[str, bool]:
    results = {}
    for assertion_name in scenario.get("assertions", []):
        fn = ALL_ASSERTIONS.get(assertion_name)
        if fn is None:
            results[assertion_name] = False
            continue

        # Some assertions need extra context
        if assertion_name == "proportional_length":
            results[assertion_name] = fn(output, scenario.get("expected_complexity", "medium"))
        else:
            results[assertion_name] = fn(output)

    return results


def run_judge(client: anthropic.Anthropic, dimension: str,
              scenario: dict, output: str) -> dict:
    module = import_module(JUDGE_MODULES[dimension])
    prompt = module.PROMPT.format(input=scenario["input"], output=output)

    response = client.messages.create(
        model=config.JUDGE_MODEL,
        max_tokens=config.JUDGE_MAX_TOKENS,
        temperature=config.JUDGE_TEMPERATURE,
        messages=[{"role": "user", "content": prompt}],
    )
    text = response.content[0].text.strip()

    # Parse JSON from response, handling markdown code blocks
    text = re.sub(r"^```json\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"score": 0, "justification": f"Failed to parse judge response: {text[:200]}"}


def run_judges(client: anthropic.Anthropic, scenario: dict, output: str) -> dict:
    results = {}
    for dimension in scenario.get("judge_dimensions", []):
        results[dimension] = run_judge(client, dimension, scenario, output)
    return results


def compute_scores(assertion_results: dict, judge_results: dict) -> dict:
    if assertion_results:
        assertion_score = sum(assertion_results.values()) / len(assertion_results)
    else:
        assertion_score = 0.0

    judge_scores = [v["score"] for v in judge_results.values() if v.get("score", 0) > 0]
    avg_judge = sum(judge_scores) / len(judge_scores) if judge_scores else 0.0
    avg_judge_normalized = avg_judge / 5.0

    composite = 0.6 * assertion_score + 0.4 * avg_judge_normalized

    return {
        "assertion_score": round(assertion_score, 4),
        "avg_judge_score": round(avg_judge, 2),
        "avg_judge_normalized": round(avg_judge_normalized, 4),
        "composite": round(composite, 4),
    }


def run_eval(skill_path: str, label: str, scenarios_dir: str, results_dir: str):
    client = anthropic.Anthropic()
    skill_content = load_skill(skill_path)
    scenarios = load_scenarios(scenarios_dir)

    print(f"Running eval: label={label}, model={config.MODEL}, scenarios={len(scenarios)}")
    print(f"Skill: {skill_path} ({len(skill_content)} chars)")
    print("=" * 70)

    all_results = []
    total_assertions = 0
    total_passed = 0
    all_judge_scores = []

    for i, scenario in enumerate(scenarios):
        name = scenario["name"]
        print(f"\n[{i+1}/{len(scenarios)}] {name} ({scenario['mode']} mode)...")

        turns = build_messages(scenario)
        start = time.time()
        output = run_conversation(client, skill_content, turns)
        elapsed = round(time.time() - start, 1)
        print(f"  Generated in {elapsed}s ({len(output.split(chr(10)))} lines)")

        assertion_results = run_assertions(output, scenario)
        passed = sum(assertion_results.values())
        total_a = len(assertion_results)
        total_assertions += total_a
        total_passed += passed
        print(f"  Assertions: {passed}/{total_a} passed")

        judge_results = run_judges(client, scenario, output)
        for dim, result in judge_results.items():
            score = result.get("score", 0)
            all_judge_scores.append(score)
            print(f"  Judge [{dim}]: {score}/5 — {result.get('justification', '')[:80]}")

        scores = compute_scores(assertion_results, judge_results)
        print(f"  Composite: {scores['composite']:.1%}")

        all_results.append({
            "id": scenario["id"],
            "name": name,
            "mode": scenario["mode"],
            "expected_complexity": scenario.get("expected_complexity"),
            "assertions": assertion_results,
            "judges": judge_results,
            "scores": scores,
            "output_lines": len(output.split("\n")),
            "elapsed_seconds": elapsed,
            "raw_output": output,
        })

    # Summary
    overall_assertion_rate = total_passed / total_assertions if total_assertions else 0
    overall_judge = sum(all_judge_scores) / len(all_judge_scores) if all_judge_scores else 0
    overall_composite = 0.6 * overall_assertion_rate + 0.4 * (overall_judge / 5.0)

    summary = {
        "assertion_pass_rate": round(overall_assertion_rate, 4),
        "avg_judge_score": round(overall_judge, 2),
        "composite_score": round(overall_composite, 4),
        "total_assertions": total_assertions,
        "total_passed": total_passed,
    }

    result_data = {
        "run_id": f"{label}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "label": label,
        "skill_path": skill_path,
        "model": config.MODEL,
        "judge_model": config.JUDGE_MODEL,
        "timestamp": datetime.now().isoformat(),
        "summary": summary,
        "scenarios": all_results,
    }

    # Save results
    out_path = Path(results_dir) / f"run_{label}.json"
    with open(out_path, "w") as f:
        json.dump(result_data, f, indent=2)

    print("\n" + "=" * 70)
    print(f"RESULTS — {label}")
    print(f"  Assertion pass rate: {summary['assertion_pass_rate']:.1%} ({total_passed}/{total_assertions})")
    print(f"  Avg judge score:     {summary['avg_judge_score']}/5")
    print(f"  Composite score:     {summary['composite_score']:.1%}")
    print(f"  Saved to: {out_path}")

    return result_data


def compare(path_a: str, path_b: str):
    with open(path_a) as f:
        a = json.load(f)
    with open(path_b) as f:
        b = json.load(f)

    print(f"Comparing: {a['label']} vs {b['label']}")
    print("=" * 70)

    # Overall
    print(f"\n{'Metric':<30} {'A (' + a['label'] + ')':<15} {'B (' + b['label'] + ')':<15} {'Delta':<10}")
    print("-" * 70)
    for key in ["assertion_pass_rate", "avg_judge_score", "composite_score"]:
        va = a["summary"][key]
        vb = b["summary"][key]
        delta = vb - va
        sign = "+" if delta > 0 else ""
        if "rate" in key or "composite" in key:
            va_s = f"{va:.1%}"
            vb_s = f"{vb:.1%}"
            d_s = f"{sign}{delta:.1%}"
        else:
            va_s = f"{va:.2f}"
            vb_s = f"{vb:.2f}"
            d_s = f"{sign}{delta:.2f}"
        print(f"  {key:<28} {va_s:<15} {vb_s:<15} {d_s}")

    # Per scenario
    print(f"\n{'Scenario':<40} {'A composite':<15} {'B composite':<15} {'Delta':<10}")
    print("-" * 80)

    a_scenarios = {s["id"]: s for s in a["scenarios"]}
    b_scenarios = {s["id"]: s for s in b["scenarios"]}

    for sid in a_scenarios:
        sa = a_scenarios[sid]
        sb = b_scenarios.get(sid)
        if not sb:
            continue
        va = sa["scores"]["composite"]
        vb = sb["scores"]["composite"]
        delta = vb - va
        sign = "+" if delta > 0 else ""
        va_s = f"{va:.1%}"
        vb_s = f"{vb:.1%}"
        d_s = f"{sign}{delta:.1%}"
        print(f"  {sa['name'][:38]:<38} {va_s:<15} {vb_s:<15} {d_s}")


def main():
    parser = argparse.ArgumentParser(description="Prompt Refiner Skill Benchmark Runner")
    parser.add_argument("--skill-path", default="SKILL.md", help="Path to the skill file")
    parser.add_argument("--label", default="run", help="Label for this benchmark run")
    parser.add_argument("--scenarios-dir", default=None, help="Path to scenarios directory")
    parser.add_argument("--results-dir", default=None, help="Path to results directory")
    parser.add_argument("--compare", nargs=2, metavar=("FILE_A", "FILE_B"),
                        help="Compare two result files")

    args = parser.parse_args()

    evals_dir = Path(__file__).parent

    if args.compare:
        compare(args.compare[0], args.compare[1])
        return

    scenarios_dir = args.scenarios_dir or str(evals_dir / "scenarios")
    results_dir = args.results_dir or str(evals_dir / "results")
    os.makedirs(results_dir, exist_ok=True)

    run_eval(args.skill_path, args.label, scenarios_dir, results_dir)


if __name__ == "__main__":
    main()
