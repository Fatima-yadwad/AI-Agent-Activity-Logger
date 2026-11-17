
from services.gemini_service import GeminiService


def test_gemini_mock_connection():

    gemini = GeminiService()

    assert gemini.mode == "mock"

    result = gemini.generate(
        prompt="Explain artificial intelligence",
        system_instruction="You are a helpful AI assistant."
    )

    assert result["text"]

    assert result["input_tokens"] > 0

    assert result["output_tokens"] > 0

    assert result["total_tokens"] == (
        result["input_tokens"]
        + result["output_tokens"]
    )

    assert result["usage_source"] == "estimated_mock"

    assert result["model"] == "mock-gemini"

    print("\nMock Gemini Test Result:")
    print(result)


def test_mock_does_not_require_real_api():

    gemini = GeminiService()

    result = gemini.generate(
        prompt="Hello Gemini"
    )

    assert "MOCK GEMINI RESPONSE" in result["text"]
