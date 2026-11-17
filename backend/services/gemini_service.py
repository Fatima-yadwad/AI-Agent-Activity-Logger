
import re
from google import genai
from google.genai import types

from config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
    LLM_MODE
)


class GeminiService:

    def __init__(self):

        self.mode = LLM_MODE
        self.model = GEMINI_MODEL

        self.client = None

        if self.mode == "real":

            self.client = genai.Client(
                api_key=GEMINI_API_KEY
            )

    def generate(
        self,
        prompt: str,
        system_instruction: str = ""
    ):

        if self.mode == "mock":
            return self._mock_generate(
                prompt,
                system_instruction
            )

        return self._real_generate(
            prompt,
            system_instruction
        )

    def _mock_generate(
        self,
        prompt: str,
        system_instruction: str
    ):

        # Local development simulation.
        # No external API request is made.

        combined = (
            system_instruction + "\n" + prompt
        )

        word_count = len(
            re.findall(r"\w+", combined)
        )

        input_tokens = max(
            1,
            (word_count + 3) // 4
        )

        response_text = (
            "[MOCK GEMINI RESPONSE]\n\n"
            "This response was generated using "
            "the local development simulator.\n\n"
            "Agent instructions:\n"
            f"{system_instruction}\n\n"
            "Processed task:\n"
            f"{prompt[:1200]}\n\n"
            "Development note: Replace mock mode "
            "with real Gemini mode before final submission."
        )

        output_tokens = max(
            1,
            (len(response_text.split()) + 3) // 4
        )

        return {
            "text": response_text,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": (
                input_tokens + output_tokens
            ),
            "usage_source": "estimated_mock",
            "model": "mock-gemini"
        }

    def _real_generate(
        self,
        prompt: str,
        system_instruction: str
    ):

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.3
            )
        )

        usage = response.usage_metadata

        input_tokens = (
            usage.prompt_token_count or 0
            if usage else 0
        )

        output_tokens = (
            usage.candidates_token_count or 0
            if usage else 0
        )

        total_tokens = (
            usage.total_token_count or 0
            if usage else 0
        )

        return {
            "text": response.text or "",
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
            "usage_source": (
                "gemini_usage_metadata"
                if usage else "unavailable"
            ),
            "model": self.model
        }
