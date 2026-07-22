from pydantic import BaseModel
from typing import List

class GeneratedFile(BaseModel):
    path: str
    content: str
    file_type: str = "python"

class AgentOutput(BaseModel):
    files: List[GeneratedFile]
