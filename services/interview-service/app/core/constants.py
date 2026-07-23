# The LLM decides each interview's actual question count (based on resume +
# role) within these bounds — not a single fixed count. Enforced both by the
# engine's structured-output schema (confirmed live: OpenAI's API genuinely
# respects Field(ge=..., le=...) here, even when explicitly prompted to
# ignore it) and defensively clamped again in code, same "don't just trust
# the model" pattern used for question_count enforcement elsewhere.
MIN_QUESTIONS = 10
MAX_QUESTIONS = 20
DEFAULT_QUESTION_COUNT = 10

DEFAULT_DIFFICULTY = "medium"