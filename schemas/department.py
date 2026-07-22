from pydantic import BaseModel
from typing import List

class Department(BaseModel):
    department_id: str
    name: str
    head_id: str
    teams: List[str]

