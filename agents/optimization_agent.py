from autogen_agentchat.agents import AssistantAgent

class OptimizationAgent(AssistantAgent):
    def __init__(self):
        super().__init__("optimization_agent", model_client=None)

    def optimize_policy(self):
        pass
