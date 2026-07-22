import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from agents.planner import PlannerAgent

planner = PlannerAgent()

plan = planner.create_plan(
    "Add coupon management",
    None,
)

print(plan.model_dump_json(indent=2))