"""Assertions for proportionality — does spec complexity match request complexity?"""

import re

# Rough line count thresholds per complexity level
THRESHOLDS = {
    "simple": (30, 250),    # min, max lines
    "medium": (80, 500),
    "complex": (150, 800),
}


def proportional_length(output: str, expected_complexity: str = "medium") -> bool:
    """Check that spec length is proportional to request complexity."""
    line_count = len(output.strip().split("\n"))
    min_lines, max_lines = THRESHOLDS.get(expected_complexity, (50, 500))
    return min_lines <= line_count <= max_lines


def no_over_engineering(output: str) -> bool:
    """For simple requests, check that the spec doesn't include enterprise features."""
    over_engineering_signals = [
        r"WebSocket",
        r"real.?time",
        r"microservice",
        r"Redis",
        r"message queue",
        r"Kafka",
        r"load balancer",
        r"CDN",
        r"Kubernetes",
        r"Docker",
        r"CI/CD pipeline",
        r"OAuth.*provider",
        r"SSO",
        r"multi.?tenant",
    ]
    matches = sum(1 for p in over_engineering_signals if re.search(p, output, re.IGNORECASE))
    # Allow up to 1 match (might be in "Out of Scope"), but 3+ is over-engineering
    return matches < 3


ASSERTIONS = {
    "proportional_length": proportional_length,
    "no_over_engineering": no_over_engineering,
}
