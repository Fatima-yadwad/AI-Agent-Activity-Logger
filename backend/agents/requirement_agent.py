
from agents.base_agent import BaseAgent


class RequirementAgent(BaseAgent):

    def __init__(self, gemini):

        super().__init__(
            name="Requirement Analyst",
            role="Requirements Analysis",

            instructions="""
You are a professional software requirements analyst.

Analyze the user's task and identify:

1. Functional requirements
2. Non-functional requirements
3. System constraints
4. Expected inputs and outputs
5. Potential edge cases
6. Assumptions and ambiguities

Present your analysis in a structured and concise format.
Do not invent requirements that are not supported by the task.
""",

            gemini=gemini
        )
