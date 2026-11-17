
import pytest

from services.gemini_service import GeminiService
from agents.requirement_agent import RequirementAgent
from agents.architect_agent import ArchitectAgent


@pytest.mark.anyio
async def test_requirement_agent():

    gemini = GeminiService()
    agent = RequirementAgent(gemini)

    result = await agent.execute(
        task="Build an AI agent activity logging system."
    )

    assert result["agent_name"] == "Requirement Analyst"
    assert result["role"] == "Requirements Analysis"
    assert result["response"]


@pytest.mark.anyio
async def test_architect_agent():

    gemini = GeminiService()
    agent = ArchitectAgent(gemini)

    result = await agent.execute(
        task="Design an AI agent activity logging system."
    )

    assert result["agent_name"] == "Software Architect"
    assert result["role"] == "System Architecture"
    assert result["response"]
