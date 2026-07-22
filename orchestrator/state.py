from typing import List
from schemas.feature_plan import FeaturePlan
from schemas.generated_file import GeneratedFile
from schemas.agent_message import AgentMessage
from scanners.convention_schema import ConventionSchema

class WorkflowState:
    def __init__(
        self,
        feature_request: str,
        conventions: ConventionSchema
    ):
        self.feature_request: str = feature_request
        self.conventions: ConventionSchema = conventions
        self.feature_plan: FeaturePlan = None
        self.generated_files: List[GeneratedFile] = []
        self.validation_errors: List[str] = []
        self.messages: List[AgentMessage] = []

    def add_message(self, msg: AgentMessage):
        self.messages.append(msg)

    def add_files(self, files: List[GeneratedFile]):
        self.generated_files.extend(files)

    def add_errors(self, errors: List[str]):
        self.validation_errors.extend(errors)
