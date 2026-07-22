from autogen_agentchat.agents import AssistantAgent

class StrategyAgent(AssistantAgent):
    def __init__(self):
        super().__init__("strategy_agent", model_client=None)

    def evaluate_strategy(self):
        pass
