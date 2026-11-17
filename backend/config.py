
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY",
    "dummy_gemini_key_for_development"
)

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)

LLM_MODE = os.getenv("LLM_MODE", "mock").lower()

if LLM_MODE not in ("mock", "real"):
    raise ValueError(
        "LLM_MODE must be either 'mock' or 'real'"
    )

if LLM_MODE == "real":
    if (
        not GEMINI_API_KEY
        or GEMINI_API_KEY.startswith("dummy_")
        or GEMINI_API_KEY.startswith("replace_")
    ):
        raise RuntimeError(
            "A real Gemini API key is required "
            "when LLM_MODE=real"
        )
