import sys
from pathlib import Path
import json

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from orchestrator.workflow import Workflow
from scanners.convention_schema import (
    ConventionSchema, ProjectInfo, FolderStructure, DatabaseConvention,
    AuthConvention, ApiConvention, FrontendConvention, ExistingModules
)

def main():
    conventions = ConventionSchema(
        project_info=ProjectInfo(name="test", backend_framework="fastapi", frontend_framework="flutter", database="postgresql"),
        folder_structure=FolderStructure(routers_path="app/modules", models_path="app/infra/models.py", screens_path="lib/screens"),
        database=DatabaseConvention(base_model_name="Base", tenant_field="tenant_id"),
        auth=AuthConvention(dependency_name="get_current_user"),
        api=ApiConvention(),
        frontend=FrontendConvention(state_management="setState"),
        existing_modules=ExistingModules()
    )

    feature = """Add coupon management with:
- fixed discounts
- percentage discounts
- expiration date
- usage limit"""

    print("Running workflow. Please wait, as this will trigger the multi-agent chat...")
    workflow = Workflow()
    result = workflow.run_workflow(feature, conventions)
    
    print("\n--- Execution Complete ---")
    print(f"Review Status: {result.review_status}")
    print(f"Total Messages: {len(result.conversation)}")
    print(f"Generated Files: {len(result.generated_files)}")
    
    print("\n[Chat Transcript]")
    for msg in result.conversation:
        print(f"[{msg.sender}] -> {msg.message[:150]}...")
        
if __name__ == "__main__":
    main()
