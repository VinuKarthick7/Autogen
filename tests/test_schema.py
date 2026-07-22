import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(PROJECT_ROOT))

from scanners.convention_schema import ConventionSchema

with open("conventions/example_conventions.json", "r") as f:
    data = json.load(f)

schema = ConventionSchema(**data)

print(schema.model_dump_json(indent=2))