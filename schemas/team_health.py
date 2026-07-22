from pydantic import BaseModel

class TeamHealth(BaseModel):
    team_id: str
    sprint_velocity: float
    burnout_risk: float
    backlog_pressure: float
    blocked_tasks: int
    morale_score: float

