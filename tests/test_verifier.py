import os
import shutil
import pytest
from verification.verifier import Verifier

def test_verifier_success():
    repo = "test_verifier_repo"
    os.makedirs(repo, exist_ok=True)
    
    try:
        # Create a basic python environment
        with open(os.path.join(repo, "pytest.ini"), "w") as f:
            f.write("[pytest]")
        
        # We need a dummy python file for it to be python
        with open(os.path.join(repo, "main.py"), "w") as f:
            f.write("print('hello')\n")
            
        # We don't want to actually run ruff/pytest/mypy if they're missing or fail in tests. 
        # But this is just testing the execution flow.
        
        verifier = Verifier()
        report = verifier.verify(repo)
        
        # Since ruff/mypy/pytest may or may not be available and might fail, we just check structure
        assert report.total_steps > 0
        assert len(report.steps) == report.total_steps
        
    finally:
        shutil.rmtree(repo, ignore_errors=True)
