from pydantic import BaseModel
from typing import Dict, Any

class KnowledgeReport(BaseModel):
    repositories_indexed: int
    patterns_discovered: int
    repair_patterns: int
    average_similarity: float
    planner_accuracy_gain: float
    repair_success_gain: float
