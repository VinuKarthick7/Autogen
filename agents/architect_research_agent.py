from autogen_agentchat.agents import AssistantAgent

class ArchitectResearchAgent(AssistantAgent):
    def __init__(self):
        super().__init__("architect_research_agent", model_client=None)

    def explore_architecture(self):
        pass
