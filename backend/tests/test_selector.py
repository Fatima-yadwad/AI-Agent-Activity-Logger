
import pytest

from services.gemini_service import GeminiService
from orchestrator.selector import SelectorOrchestrator


@pytest.mark.anyio
async def test_selector_selects_architect():

    gemini = GeminiService()
    orchestrator = SelectorOrchestrator(gemini)

    result = await orchestrator.execute(
        task="Design the system architecture and database."
    )

    assert result["mode"] == "selector"
    assert result["selected_agent"] == "Software Architect"
    assert len(result["results"]) == 1
    assert result["events"][0]["status"] == "completed"


@pytest.mark.anyio
async def test_selector_selects_requirement_agent():

    gemini = GeminiService()
    orchestrator = SelectorOrchestrator(gemini)

    result = await orchestrator.execute(
        task="Identify functional and non-functional requirements."
    )

    assert result["mode"] == "selector"
    assert result["selected_agent"] == "Requirement Analyst"
    assert len(result["results"]) == 1


def test_selector_routing_is_deterministic():

    gemini = GeminiService()
    orchestrator = SelectorOrchestrator(gemini)

    first_selection = orchestrator.select_agent(
        "Design the system architecture."
    )

    second_selection = orchestrator.select_agent(
        "Design the system architecture."
    )

    assert first_selection.name == second_selection.name
