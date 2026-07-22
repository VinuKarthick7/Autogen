from autogen_agentchat.agents import AssistantAgent

class ExperimentAgent(AssistantAgent):
    def __init__(self):
        super().__init__("experiment_agent", model_client=None)

    def run_experiment(self):
        pass
