
from agents.base_agent import BaseAgent


class ArchitectAgent(BaseAgent):

    def __init__(self, gemini):

        super().__init__(
            name="Software Architect",
            role="System Architecture",

            instructions="""
You are a senior software architect.

Based on the provided task and requirements:

1. Identify the major system components.
2. Define component responsibilities.
3. Describe interactions between components.
4. Recommend suitable technologies.
5. Define important API interfaces.
6. Identify scalability and security considerations.
7. Highlight architectural trade-offs.

Provide a structured architecture proposal.
Use the supplied requirements as the source of truth.
""",

            gemini=gemini
        )
