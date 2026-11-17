
import asyncio

from services.gemini_service import GeminiService


class BaseAgent:
    """
    Foundation for all agents in the activity-logging system.

    Each agent has a name, role, and set of instructions.
    It delegates text generation to GeminiService.
    """

    def __init__(
        self,
        name: str,
        role: str,
        instructions: str,
        gemini: GeminiService
    ):
        self.name = name
        self.role = role
        self.instructions = instructions
        self.gemini = gemini

    async def execute(
        self,
        task: str,
        context: str = ""
    ) -> dict:
        """
        Execute an assigned task and return a structured result.
        """

        prompt = f"""
Task:
{task}

Previous context:
{context}

Your responsibility:
{self.instructions}

Complete your assigned task.
Return a clear and useful response.
"""

        result = await asyncio.to_thread(
            self.gemini.generate,
            prompt,
            self.instructions
        )

        return {
            "agent_name": self.name,
            "role": self.role,
            "response": result["text"],
            "usage": {
                "input_tokens": result["input_tokens"],
                "output_tokens": result["output_tokens"],
                "total_tokens": result["total_tokens"],
                "usage_source": result["usage_source"]
            }
        }
