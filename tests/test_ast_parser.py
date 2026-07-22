import sys
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scanners.ast_parser import extract_models

def test_ast_parser():
    file_path = r"C:\projects\PMS\pinesphere_backend\app\infra\models.py"
    models = extract_models(file_path)
    print(json.dumps(models, indent=2))

if __name__ == "__main__":
    test_ast_parser()
