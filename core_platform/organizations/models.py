from pydantic import BaseModel
from typing import List, Optional

class TeamModel(BaseModel):
    team_id: str
    name: str
    members: List[str]

class OrganizationModel(BaseModel):
    org_id: str
    name: str
    billing_plan: str
    teams: List[TeamModel]
