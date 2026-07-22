from pydantic import BaseModel

class RepairPattern(BaseModel):
    pattern_id: str
    category: str
    repositories: list[str]
    trigger: str
    repair_strategy: str
    success_rate: float
    average_repair_depth: float
