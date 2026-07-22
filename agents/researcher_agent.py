from autogen_agentchat.agents import AssistantAgent

class ResearcherAgent(AssistantAgent):
    def __init__(self):
        super().__init__("researcher_agent", model_client=None)

    def generate_hypothesis(self):
        pass
