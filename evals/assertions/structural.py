"""Programmatic assertions for spec structural completeness."""

import re


def has_overview(output: str) -> bool:
    return bool(re.search(r"##\s+Overview", output))


def has_tech_stack(output: str) -> bool:
    return bool(re.search(r"##\s+Tech Stack", output))


def has_data_model(output: str) -> bool:
    if not re.search(r"##\s+Data Model", output):
        return False
    # Must have at least one entity defined
    return bool(re.search(r"###\s+\w+", output[output.find("Data Model"):]))


def has_user_flows(output: str) -> bool:
    if not re.search(r"##\s+User Flows", output):
        return False
    # Must have numbered steps
    return bool(re.search(r"\d+\.\s+", output[output.find("User Flows"):]))


def has_features(output: str) -> bool:
    return bool(re.search(r"##\s+Features", output))


def has_validation_rules(output: str) -> bool:
    return bool(re.search(r"(?:##\s+Validation|validation rule)", output, re.IGNORECASE))


def has_error_handling(output: str) -> bool:
    return bool(re.search(r"(?:##\s+Error Handling|error handling)", output, re.IGNORECASE))


def has_assumptions(output: str) -> bool:
    if not re.search(r"##\s+Assumptions", output):
        return False
    # Must have at least 2 assumption items
    assumptions_section = output[output.find("## Assumptions"):]
    next_section = re.search(r"\n##\s+", assumptions_section[3:])
    if next_section:
        assumptions_section = assumptions_section[:next_section.start() + 3]
    items = re.findall(r"^[-*]\s+", assumptions_section, re.MULTILINE)
    return len(items) >= 2


def has_out_of_scope(output: str) -> bool:
    return bool(re.search(r"##\s+Out of Scope", output))


def has_self_assessment(output: str) -> bool:
    if not re.search(r"##\s+Self-Assessment", output):
        return False
    # Must have numerical ratings
    return bool(re.search(r"\d\s*/\s*5", output))


def has_builder_notes(output: str) -> bool:
    return bool(re.search(r"##\s+Builder Notes", output))


def has_future_considerations(output: str) -> bool:
    return bool(re.search(r"##\s+Future Considerations", output))


ASSERTIONS = {
    "has_overview": has_overview,
    "has_tech_stack": has_tech_stack,
    "has_data_model": has_data_model,
    "has_user_flows": has_user_flows,
    "has_features": has_features,
    "has_validation_rules": has_validation_rules,
    "has_error_handling": has_error_handling,
    "has_assumptions": has_assumptions,
    "has_out_of_scope": has_out_of_scope,
    "has_self_assessment": has_self_assessment,
    "has_builder_notes": has_builder_notes,
    "has_future_considerations": has_future_considerations,
}
