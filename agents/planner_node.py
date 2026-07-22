import os
from autogen_agentchat.agents import AssistantAgent
from orchestrator.gemini_client import GeminiClient
from scanners.convention_schema import ConventionSchema
from schemas.feature_plan import FeaturePlan

class PlannerAgentNode(AssistantAgent):
    def __init__(self, conventions: ConventionSchema, plan: FeaturePlan):
        client = GeminiClient(
            model_name=os.getenv("MODEL_NAME", "gemini-1.5-flash"),
            api_key=os.getenv("GEMINI_API_KEY")
        )
        sys_msg = f"""You are the Planner Agent.
Your role is to orchestrate the plan.
The current feature plan is:
{plan.model_dump_json()}

Instructions:
Announce the plan to the team. Tell the database agent to begin generating models.
"""
        super().__init__(
            name="planner",
            model_client=client,
            system_message=sys_msg,
            description="Analyzes the feature and distributes the FeaturePlan to the team."
        )
