import os
import shutil
from verification.test_runner import TestRunner

def test_test_runner_detection():
    repo = "test_test_runner_repo"
    os.makedirs(repo, exist_ok=True)
    
    try:
        runner = TestRunner(repo)
        assert runner.detect_framework() is None
        
        with open(os.path.join(repo, "pubspec.yaml"), "w") as f:
            f.write("name: test")
        assert runner.detect_framework() == "flutter"
        os.remove(os.path.join(repo, "pubspec.yaml"))
        
        with open(os.path.join(repo, "package.json"), "w") as f:
            f.write("{}")
        assert runner.detect_framework() == "node"
        os.remove(os.path.join(repo, "package.json"))
        
        with open(os.path.join(repo, "pytest.ini"), "w") as f:
            f.write("[pytest]")
        assert runner.detect_framework() == "python"
        
    finally:
        shutil.rmtree(repo, ignore_errors=True)
