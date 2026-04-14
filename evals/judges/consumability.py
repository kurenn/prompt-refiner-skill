"""LLM-as-judge: evaluates whether the spec is well-structured for an AI builder."""

PROMPT = """\
You are an AI coding assistant about to build an application from the following specification. \
Rate how well-structured it is for you to follow.

**Specification:**
{output}

Rate BUILDER CONSUMABILITY on a 1-5 scale:

1 = Poorly structured — would need to constantly cross-reference between sections, unclear \
implementation order, ambiguous requirements, excessive length without clear priorities.
2 = Somewhat followable but has significant gaps — some TBD items, forward references to \
later sections, requirements scattered across distant sections.
3 = Adequate — clear implementation order, most requirements are findable, but some \
cross-referencing needed. Could build from this with occasional guessing.
4 = Well-structured — phases are independently buildable, requirements are colocated with \
their implementation steps, self-contained with no TBDs. Could build confidently.
5 = Excellent — each phase is independently buildable with no forward references, critical \
vs. polish requirements are clearly distinguished, spec length is proportional to \
complexity, every requirement has enough detail to implement without guessing.

Respond with ONLY valid JSON:
{{"score": <1-5>, "justification": "<2-3 sentences explaining the rating>"}}
"""

DIMENSION = "consumability"
