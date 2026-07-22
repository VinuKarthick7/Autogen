from pydantic import BaseModel
from typing import List

class Employee(BaseModel):
    employee_id: str
    name: str
    role: str
    level: str
    skills: List[str]
    team_id: str | None

