
from agents.requirement_agent import RequirementAgent
from agents.architect_agent import ArchitectAgent
from services.gemini_service import GeminiService


class ConversationOrchestrator:

    def __init__(self, gemini: GeminiService):

        self.requirement_agent = RequirementAgent(gemini)
        self.architect_agent = ArchitectAgent(gemini)

    async def execute(self, task: str) -> dict:

        events = []
        results = []

        # Agent 1: Requirement Analysis
        requirement_result = await self.requirement_agent.execute(
            task=task
        )

        results.append(requirement_result)

        events.append({
            "event_type": "agent_action",
            "agent_name": requirement_result["agent_name"],
            "action": "Analyzed user requirements",
            "status": "completed"
        })

        # Agent 2: Software Architecture
        architecture_result = await self.architect_agent.execute(
            task=task,
            context=requirement_result["response"]
        )

        results.append(architecture_result)

        events.append({
            "event_type": "agent_action",
            "agent_name": architecture_result["agent_name"],
            "action": "Designed system architecture",
            "status": "completed"
        })

        # Aggregate token usage
        total_input_tokens = sum(
            result["usage"]["input_tokens"]
            for result in results
        )

        total_output_tokens = sum(
            result["usage"]["output_tokens"]
            for result in results
        )

        total_tokens = sum(
            result["usage"]["total_tokens"]
            for result in results
        )

        return {
            "mode": "conversation",
            "task": task,
            "results": results,
            "events": events,
            "usage": {
                "input_tokens": total_input_tokens,
                "output_tokens": total_output_tokens,
                "total_tokens": total_tokens,
                "usage_source": "estimated_mock"
            }
        }
