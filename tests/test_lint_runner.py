import os
import shutil
from verification.lint_runner import LintRunner

def test_lint_runner_detection():
    repo = "test_lint_runner_repo"
    os.makedirs(repo, exist_ok=True)
    
    try:
        runner = LintRunner(repo)
        assert runner.detect_framework() is None
        
        with open(os.path.join(repo, "pubspec.yaml"), "w") as f:
            f.write("name: test")
        assert runner.detect_framework() == "flutter"
        
    finally:
        shutil.rmtree(repo, ignore_errors=True)
