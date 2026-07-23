from functools import lru_cache

from openai import OpenAI

from app.core.config import get_settings

# Confirmed against a real call: gpt-4o-mini (the model named in
# architecture.png) no longer exists in the API as of this build — the
# lineup has moved to GPT-5.x. gpt-5.4-mini is the direct equivalent
# (mid-tier, cost-effective) and is what every engine module targets.
MODEL = "gpt-5.4-mini"


@lru_cache
def get_openai_client() -> OpenAI:
    return OpenAI(api_key=get_settings().openai_api_key)