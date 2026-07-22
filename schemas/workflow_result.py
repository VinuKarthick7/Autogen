from pydantic import BaseModel
from typing import List
from schemas.feature_plan import FeaturePlan
from schemas.generated_file import GeneratedFile
from schemas.agent_message import AgentMessage

class WorkflowResult(BaseModel):
    plan: FeaturePlan
    generated_files: List[GeneratedFile]
    review_status: str
    validation_errors: List[str]
    conversation: List[AgentMessage]
