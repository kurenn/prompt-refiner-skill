"""Assertions for mode compliance — did the skill follow the requested mode?"""

import re


def mode_one_shot_compliant(output: str) -> bool:
    """One-shot mode: produces a full spec without asking questions first."""
    # Should have a data model or features section (produced a spec)
    has_spec = bool(re.search(r"##\s+(?:Data Model|Features|Overview)", output))
    # Should NOT start with questions before producing the spec
    # Check if the first substantial content is questions rather than a spec
    lines = output.strip().split("\n")
    first_50 = "\n".join(lines[:50])
    starts_with_questions = bool(
        re.search(r"(?:before I|let me ask|I have.*questions|I'd like to ask)", first_50, re.IGNORECASE)
    )
    return has_spec and not starts_with_questions


def mode_interactive_compliant(output: str) -> bool:
    """Interactive mode: asks questions BEFORE producing a full spec."""
    # Should contain questions (? marks in the first response)
    has_questions = output.count("?") >= 2
    # Should NOT immediately produce a full spec with data model
    # The first response should be questions, not a spec
    first_500_chars = output[:500]
    has_immediate_spec = bool(re.search(r"##\s+Data Model", first_500_chars))
    return has_questions and not has_immediate_spec


def mode_hybrid_compliant(output: str) -> bool:
    """Hybrid mode: produces a draft spec, THEN asks follow-up questions."""
    has_spec = bool(re.search(r"##\s+(?:Data Model|Features|Overview)", output))
    has_questions = output.count("?") >= 2
    return has_spec and has_questions


ASSERTIONS = {
    "mode_one_shot_compliant": mode_one_shot_compliant,
    "mode_interactive_compliant": mode_interactive_compliant,
    "mode_hybrid_compliant": mode_hybrid_compliant,
}
