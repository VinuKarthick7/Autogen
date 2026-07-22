from autogen_agentchat.agents import AssistantAgent

class PerformanceAgent(AssistantAgent):
    def __init__(self):
        super().__init__("performance_agent", model_client=None)

    def analyze_performance(self):
        pass

    def estimate_load(self):
        pass

    def find_bottlenecks(self):
        pass
