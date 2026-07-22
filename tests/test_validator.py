import sys
from pathlib import Path
import json

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from validators.convention_validator import ConventionValidator
from schemas.generated_file import AgentOutput, GeneratedFile
from scanners.convention_schema import (
    ConventionSchema, ProjectInfo, FolderStructure, DatabaseConvention,
    AuthConvention, ApiConvention, FrontendConvention, ExistingModules
)

def main():
    validator = ConventionValidator()
    conventions = ConventionSchema(
        project_info=ProjectInfo(name="test", backend_framework="fastapi", frontend_framework="flutter", database="postgresql"),
        folder_structure=FolderStructure(routers_path="app/modules", models_path="app/models", screens_path="lib/screens"),
        database=DatabaseConvention(base_model_name="Base", tenant_field="tenant_id"),
        auth=AuthConvention(dependency_name="get_current_user"),
        api=ApiConvention(),
        frontend=FrontendConvention(state_management="setState"),
        existing_modules=ExistingModules()
    )

    valid_output = AgentOutput(
        files=[
            GeneratedFile(
                path="app/models/coupon.py",
                content="from sqlalchemy import Column, Integer\nfrom app.database import Base\nimport uuid\nfrom sqlalchemy.orm import Mapped, mapped_column\nclass Coupon(Base):\n    tenant_id: Mapped[uuid.UUID] = mapped_column()",
                file_type="python"
            ),
            GeneratedFile(
                path="app/modules/coupons/router.py",
                content="from fastapi import APIRouter, Depends\nfrom app.dependencies import get_current_user\nrouter = APIRouter()\ndef create_coupon(user = Depends(get_current_user)):\n    pass\n",
                file_type="python"
            ),
            GeneratedFile(
                path="lib/screens/coupon_screen.dart",
                content="import 'package:flutter/material.dart';\nclass CouponScreen extends StatelessWidget {}",
                file_type="dart"
            )
        ]
    )
    
    invalid_output = AgentOutput(
        files=[
            GeneratedFile(
                path="app/models/coupon.py",
                content="class Coupon:\n    id = Column(Integer)\n    # using sqlalchemy to trigger db check\n    # sqlalchemy",
                file_type="python"
            ),
            GeneratedFile(
                path="routes/coupon_router.py",
                content="from fastapi import APIRouter\nrouter = APIRouter()",
                file_type="python"
            ),
            GeneratedFile(
                path="ui/coupon_screen.dart",
                content="class CouponScreen {}",
                file_type="dart"
            )
        ]
    )

    print("Validating valid output:")
    valid_res = validator.validate(valid_output, conventions)
    print(json.dumps(valid_res, indent=2))
    
    print("\nValidating invalid output:")
    invalid_res = validator.validate(invalid_output, conventions)
    print(json.dumps(invalid_res, indent=2))

if __name__ == "__main__":
    main()
