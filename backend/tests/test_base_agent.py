
import pytest

from agents.base_agent import BaseAgent
from services.gemini_service import GeminiService


@pytest.mark.anyio
async def test_base_agent_execution():

    gemini = GeminiService()

    agent = BaseAgent(
        name="Test Agent",
        role="General Assistant",
        instructions="You are a helpful AI assistant.",
        gemini=gemini
    )

    result = await agent.execute(
        task="Explain what an AI agent is."
    )

    assert result["agent_name"] == "Test Agent"
    assert result["role"] == "General Assistant"
    assert result["response"]
    assert result["usage"]["total_tokens"] > 0
    assert result["usage"]["usage_source"] == "estimated_mock"
