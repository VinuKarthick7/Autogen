from pydantic import BaseModel
from schemas.verification_step import VerificationStep

class VerificationReport(BaseModel):
    passed: bool
    total_steps: int
    passed_steps: int
    failed_steps: int
    steps: list[VerificationStep]
    rule_violations: list[dict] = [] # dict of RuleViolation
