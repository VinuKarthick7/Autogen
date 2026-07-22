from pydantic import BaseModel
from typing import List

class Innovation(BaseModel):
    id: str
    name: str
    description: str
    combined_strategies: List[str]
    novelty_score: float
