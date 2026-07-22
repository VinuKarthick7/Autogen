import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(PROJECT_ROOT))

from scanners.python_scanner import PythonConventionScanner

scanner = PythonConventionScanner(
    r"C:\projects\PMS\pinesphere_backend"
)

result = scanner.scan()

print(result.model_dump_json(indent=2))