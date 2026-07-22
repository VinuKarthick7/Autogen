import sys
from pathlib import Path
import json

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from orchestrator.workflow import Workflow

if __name__ == "__main__":
    workflow = Workflow()
    result = workflow.run("Add coupon management")
    print(json.dumps(result, indent=2))
