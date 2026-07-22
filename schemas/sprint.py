from pydantic import BaseModel
from datetime import datetime

class Sprint(BaseModel):
    sprint_id: str
    team_id: str
    start_date: datetime
    end_date: datetime
    status: str
    capacity: float
    completed_points: float | None

