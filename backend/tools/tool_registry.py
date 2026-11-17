
class ToolRegistry:

    def __init__(self):
        self.tools = {}

    def register(self, name: str, tool):
        if name in self.tools:
            raise ValueError(f"Tool already registered: {name}")

        self.tools[name] = tool

    def execute(self, name: str, **kwargs):

        if name not in self.tools:
            raise ValueError(f"Unknown tool: {name}")

        return self.tools[name].calculate(**kwargs)

    def list_tools(self):
        return list(self.tools.keys())

