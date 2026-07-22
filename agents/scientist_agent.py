from autogen_agentchat.agents import AssistantAgent

class ScientistAgent(AssistantAgent):
    def __init__(self):
        super().__init__("scientist_agent", model_client=None)

    def analyze_results(self):
        pass
