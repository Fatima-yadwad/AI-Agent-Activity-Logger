
import pytest

from services.gemini_service import GeminiService
from agents.requirement_agent import RequirementAgent
from agents.architect_agent import ArchitectAgent
from orchestrator.round_robin import RoundRobinOrchestrator


@pytest.mark.anyio
async def test_round_robin_execution():

    gemini = GeminiService()

    agents = [
        RequirementAgent(gemini),
        ArchitectAgent(gemini)
    ]

    orchestrator = RoundRobinOrchestrator(agents)

    result = await orchestrator.execute(
        task="Develop an AI agent activity logging system.",
        rounds=2
    )

    assert result["mode"] == "round_robin"
    assert result["rounds"] == 2

    # Two agents execute in each of two rounds.
    assert len(result["results"]) == 4
    assert len(result["events"]) == 4

    assert result["results"][0]["agent_name"] == "Requirement Analyst"
    assert result["results"][1]["agent_name"] == "Software Architect"
    assert result["results"][2]["agent_name"] == "Requirement Analyst"
    assert result["results"][3]["agent_name"] == "Software Architect"

    assert result["usage"]["total_tokens"] > 0


@pytest.mark.anyio
async def test_round_robin_rejects_zero_rounds():

    gemini = GeminiService()

    orchestrator = RoundRobinOrchestrator([
        RequirementAgent(gemini)
    ])

    with pytest.raises(ValueError):
        await orchestrator.execute(
            task="Test task",
            rounds=0
        )
