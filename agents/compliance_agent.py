from autogen_agentchat.agents import AssistantAgent

class ComplianceAgent(AssistantAgent):
    def __init__(self):
        super().__init__("compliance_agent", model_client=None)

    def check_compliance(self):
        pass

    def generate_report(self):
        pass
