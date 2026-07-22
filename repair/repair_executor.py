import json
from typing import List, Optional
from repair.repair_policy import RepairPolicy
from repair.repair_plan import RepairPlan
from repair.repair_step import RepairStep
from repair.repair_history import RepairHistory
from schemas.verification_report import VerificationReport
from schemas.rule_violation import RuleViolation

class RepairExecutor:
    def __init__(self):
        self.policy = RepairPolicy()

    def evaluate_failures(self, report: VerificationReport, history: RepairHistory) -> Optional[RepairPlan]:
        if report.passed:
            return None
            
        # Parse failures from rule violations and failed steps
        failures = []
        for v_dict in report.rule_violations:
            violations = RuleViolation(**v_dict)
            failures.append(violations)
            
        # Add linting/build failures if present
        for step in report.steps:
            if not step.success and step.name not in ["Rules Engine"]:
                # Synthesize a generic RuleViolation for the step failure
                failures.append(RuleViolation(
                    severity="HIGH",
                    category=step.name.upper(), # e.g. LINT
                    file="various",
                    line=0,
                    message=f"{step.name} failed",
                    suggestion="Fix compile/lint errors"
                ))

        if not failures:
            return None

        steps = []
        min_max_attempts = 3
        
        for idx, failure in enumerate(failures):
            category = failure.category
            if not self.policy.can_auto_repair(category):
                print(f"[REPAIR] Blocked: Category {category} cannot be auto-repaired (SECURITY/REGRESSION).")
                return None
                
            attempts = self.policy.get_max_attempts(category)
            if attempts < min_max_attempts:
                min_max_attempts = attempts
                
            steps.append(
                RepairStep(
                    id=f"step_{idx}",
                    category=category,
                    target_files=[failure.file],
                    description=f"Repair {category} violation in {failure.file}",
                    reason=failure.message,
                    blocking=failure.severity in ["CRITICAL", "HIGH"]
                )
            )

        if not history.can_repair(max_attempts=min_max_attempts):
            print(f"[REPAIR] Blocked: Exceeded max attempts ({min_max_attempts}) or depth limits.")
            return None

        return RepairPlan(
            failures=failures,
            steps=steps,
            max_attempts=min_max_attempts
        )
