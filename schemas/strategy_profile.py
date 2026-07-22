from pydantic import BaseModel
from typing import Literal, List

class StrategyProfile(BaseModel):
    strategy_id: str
    strategy_type: Literal[
        "planner",
        "repair",
        "retrieval",
        "verification"
    ]
    repositories: List[str]
    success_rate: float
    average_runtime: float
    average_repair_depth: float
    average_cost: float
