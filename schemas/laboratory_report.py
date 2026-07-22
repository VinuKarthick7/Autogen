from pydantic import BaseModel
from typing import List

class LaboratoryReport(BaseModel):
    id: str
    title: str
    summary: str
    active_experiments: int
    recent_discoveries: List[str]
