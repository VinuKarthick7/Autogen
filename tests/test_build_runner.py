import os
import shutil
from verification.build_runner import BuildRunner

def test_build_runner_detection():
    repo = "test_build_runner_repo"
    os.makedirs(repo, exist_ok=True)
    
    try:
        runner = BuildRunner(repo)
        assert runner.detect_framework() is None
        
        with open(os.path.join(repo, "package.json"), "w") as f:
            f.write("{}")
        assert runner.detect_framework() == "node"
        
    finally:
        shutil.rmtree(repo, ignore_errors=True)
