
from typing import Sequence

from agents.base_agent import BaseAgent


class RoundRobinOrchestrator:

    def __init__(self, agents: Sequence[BaseAgent]):
        if not agents:
            raise ValueError("At least one agent is required.")

        self.agents = list(agents)

    async def execute(
        self,
        task: str,
        rounds: int = 1
    ) -> dict:

        if rounds < 1:
            raise ValueError("Rounds must be at least 1.")

        context = ""
        results = []
        events = []

        for round_number in range(1, rounds + 1):

            for agent in self.agents:

                result = await agent.execute(
                    task=task,
                    context=context
                )

                results.append(result)

                context = result["response"]

                events.append({
                    "event_type": "agent_action",
                    "agent_name": result["agent_name"],
                    "action": "Executed Round Robin turn",
                    "round": round_number,
                    "status": "completed"
                })

        total_input_tokens = sum(
            item["usage"]["input_tokens"]
            for item in results
        )

        total_output_tokens = sum(
            item["usage"]["output_tokens"]
            for item in results
        )

        total_tokens = sum(
            item["usage"]["total_tokens"]
            for item in results
        )

        return {
            "mode": "round_robin",
            "task": task,
            "rounds": rounds,
            "results": results,
            "events": events,
            "usage": {
                "input_tokens": total_input_tokens,
                "output_tokens": total_output_tokens,
                "total_tokens": total_tokens,
                "usage_source": "estimated_mock"
            }
        }
