from pydantic import BaseModel
from typing import List

class Experiment(BaseModel):
    id: str
    hypothesis_id: str
    control_group: str
    experimental_group: str
    success_metrics: List[str]
    failure_conditions: List[str]
    status: str
