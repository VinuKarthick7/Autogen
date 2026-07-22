import os
import json
from autogen_agentchat.agents import AssistantAgent
from orchestrator.gemini_client import GeminiClient
from scanners.convention_schema import ConventionSchema
from schemas.feature_plan import FeaturePlan
from schemas.generated_file import AgentOutput
from schemas.verification_report import VerificationReport
from validators.convention_validator import ConventionValidator

class ReviewerAgent(AssistantAgent):
    def __init__(self, conventions: ConventionSchema, plan: FeaturePlan, verification_report: VerificationReport = None):
        client = GeminiClient(
            model_name=os.getenv("MODEL_NAME", "gemini-1.5-flash"),
            api_key=os.getenv("GEMINI_API_KEY")
        )
        report_str = verification_report.model_dump_json(indent=2) if verification_report else "{}"
        sys_msg = f"""You are the Reviewer Agent.
Your job is to validate the generated code and the verification report.
Look at the Verification Report provided to you. 
If passed is true and there are no CRITICAL or HIGH rule violations, output exactly the word "APPROVE".
If it returns errors, passed is false, or there are CRITICAL/HIGH rule violations, output "REJECT" and list the failed steps or violations.

Verification Report:
{report_str}
"""
        
        super().__init__(
            name="reviewer",
            model_client=client,
            system_message=sys_msg,
            description="Reviews generated files using the Verification Report.",
        )
