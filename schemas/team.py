from pydantic import BaseModel
from typing import Literal

class Team(BaseModel):
    team_id: str
    name: str
    type: Literal['backend', 'frontend', 'qa', 'devops', 'sre', 'product']
    lead: str
    members: list[str]
    velocity: float
    active_sprint: str | None

