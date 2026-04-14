import os

MODEL = os.environ.get("EVAL_MODEL", "claude-sonnet-4-20250514")
JUDGE_MODEL = os.environ.get("EVAL_JUDGE_MODEL", "claude-sonnet-4-20250514")
MAX_TOKENS = 8192
TEMPERATURE = 0
JUDGE_MAX_TOKENS = 1024
JUDGE_TEMPERATURE = 0
