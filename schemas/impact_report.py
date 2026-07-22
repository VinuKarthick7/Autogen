from dataclasses import dataclass
from typing import List

@dataclass
class ImpactReport:
    feature_request: str
    affected_files: List[str]
    reasoning: str
