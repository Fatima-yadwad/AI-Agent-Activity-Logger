
from agents.requirement_agent import RequirementAgent
from agents.architect_agent import ArchitectAgent
from services.gemini_service import GeminiService


class SelectorOrchestrator:

    def __init__(self, gemini: GeminiService):

        self.requirement_agent = RequirementAgent(gemini)
        self.architect_agent = ArchitectAgent(gemini)

    def select_agent(self, task: str):

        task_lower = task.lower()

        architecture_keywords = [
            "architecture",
            "design",
            "system design",
            "database",
            "api",
            "technology",
            "infrastructure",
            "components"
        ]

        if any(
            keyword in task_lower
            for keyword in architecture_keywords
        ):
            return self.architect_agent

        return self.requirement_agent

    async def execute(self, task: str) -> dict:

        selected_agent = self.select_agent(task)

        result = await selected_agent.execute(
            task=task
        )

        return {
            "mode": "selector",
            "task": task,
            "selected_agent": selected_agent.name,
            "results": [result],
            "events": [
                {
                    "event_type": "agent_action",
                    "agent_name": selected_agent.name,
                    "action": "Selected and executed agent",
                    "status": "completed"
                }
            ],
            "usage": result["usage"]
        }
