
import pytest

from services.gemini_service import GeminiService
from orchestrator.conversation import ConversationOrchestrator


@pytest.mark.anyio
async def test_conversation_execution():

    gemini = GeminiService()

    orchestrator = ConversationOrchestrator(gemini)

    result = await orchestrator.execute(
        task="Develop an AI agent activity logging system."
    )

    assert result["mode"] == "conversation"

    assert len(result["results"]) == 2
    assert len(result["events"]) == 2

    assert (
        result["results"][0]["agent_name"]
        == "Requirement Analyst"
    )

    assert (
        result["results"][1]["agent_name"]
        == "Software Architect"
    )

    assert result["usage"]["total_tokens"] > 0

    assert all(
        event["status"] == "completed"
        for event in result["events"]
    )
