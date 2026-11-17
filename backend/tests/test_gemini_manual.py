
from services.gemini_service import GeminiService

gemini = GeminiService()

print("LLM Mode:", gemini.mode)

result = gemini.generate(
    prompt="Explain what an AI agent is",
    system_instruction="You are an AI assistant."
)

print("\nGenerated Response:")
print(result["text"])

print("\nToken Statistics:")
print("Input Tokens:", result["input_tokens"])
print("Output Tokens:", result["output_tokens"])
print("Total Tokens:", result["total_tokens"])

print("\nUsage Source:", result["usage_source"])
