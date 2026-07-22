from autogen_agentchat.agents import AssistantAgent

class IncidentAgent(AssistantAgent):
    def __init__(self):
        super().__init__("incident_agent", model_client=None)

    def detect_incident(self):
        pass

    def correlate_services(self):
        pass

    def create_incident(self):
        pass
