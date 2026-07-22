import sys
from pathlib import Path
import json

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from agents.planner import PlannerAgent
from scanners.convention_schema import (
    ConventionSchema, ProjectInfo, FolderStructure, DatabaseConvention,
    AuthConvention, ApiConvention, FrontendConvention, ExistingModules
)

def main():
    planner = PlannerAgent()
    conventions = ConventionSchema(
        project_info=ProjectInfo(name="test", backend_framework="fastapi", frontend_framework="flutter", database="postgresql"),
        folder_structure=FolderStructure(routers_path="app/modules", models_path="app/infra/models.py", screens_path="lib/screens"),
        database=DatabaseConvention(base_model_name="Base", tenant_field="tenant_id"),
        auth=AuthConvention(dependency_name="get_current_user"),
        api=ApiConvention(),
        frontend=FrontendConvention(state_management="setState"),
        existing_modules=ExistingModules()
    )

    request = """Add coupon management with:
- percentage discounts
- fixed discounts
- expiration date
- usage limit"""

    plan = planner.create_plan(request, conventions)
    print(plan.model_dump_json(indent=2))

if __name__ == "__main__":
    main()
