from pydantic import BaseModel
from typing import Literal

class InfrastructureCost(BaseModel):
    cost_id: str
    service: str
    category: Literal[
        "compute",
        "database",
        "storage",
        "bandwidth"
    ]
    amount_usd: float
