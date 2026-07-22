from dataclasses import dataclass
from typing import List

@dataclass
class RepairStep:
    id: str
    category: str
    target_files: List[str]
    description: str
    reason: str
    blocking: bool
