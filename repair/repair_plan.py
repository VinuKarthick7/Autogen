from dataclasses import dataclass
from typing import List
from schemas.rule_violation import RuleViolation
from repair.repair_step import RepairStep

@dataclass
class RepairPlan:
    failures: List[RuleViolation]
    steps: List[RepairStep]
    max_attempts: int
