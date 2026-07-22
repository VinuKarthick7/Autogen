from pydantic import BaseModel
from typing import List

class ProjectModel(BaseModel):
    project_id: str
    org_id: str
    name: str
    repositories: List[str]
