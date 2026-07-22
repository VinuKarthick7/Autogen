from schemas.verification_report import VerificationReport
from schemas.verification_step import VerificationStep
from verification.lint_runner import LintRunner
from verification.build_runner import BuildRunner
from verification.migration_runner import MigrationRunner
from verification.test_runner import TestRunner
import time

class Verifier:
    def verify(self, workspace_path: str) -> VerificationReport:
        runners = [
            ("Lint", LintRunner(workspace_path)),
            ("Build", BuildRunner(workspace_path)),
            ("Migration", MigrationRunner(workspace_path)),
            ("Tests", TestRunner(workspace_path))
        ]
        
        steps = []
        passed_steps = 0
        failed_steps = 0
        passed = True
        
        for name, runner in runners:
            success, duration, stdout, stderr = runner.run()
            
            step = VerificationStep(
                name=name,
                command="auto-detected",
                success=success,
                duration_ms=duration,
                stdout=stdout,
                stderr=stderr
            )
            steps.append(step)
            
            if success:
                passed_steps += 1
            else:
                failed_steps += 1
                passed = False
                break # Stop immediately on catastrophic failure
                
        return VerificationReport(
            passed=passed,
            total_steps=len(steps),
            passed_steps=passed_steps,
            failed_steps=failed_steps,
            steps=steps
        )
