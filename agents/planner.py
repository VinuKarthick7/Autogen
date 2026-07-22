
import os
import json
import logging
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import ValidationError

from schemas.feature_plan import FeaturePlan
from scanners.convention_schema import ConventionSchema

# Configure logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/planner.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("PlannerAgent")

class PlannerAgent:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env")
        self.client = genai.Client(api_key=api_key)
        self.model_name = os.getenv("MODEL_NAME", "gemini-2.5-flash")

    def _build_prompt(self, feature_request: str, conventions: ConventionSchema) -> str:
        prompt = f"""You are a principal software architect.

Generate an implementation plan that strictly follows:
- existing modules
- project conventions
- database patterns
- authentication system
- routing structure

Return ONLY valid JSON matching the FeaturePlan schema.

Feature Request:
{feature_request}

Conventions:
{conventions.model_dump_json(indent=2)}
"""
        return prompt

    def normalize_plan(
        self,
        plan: FeaturePlan,
        conventions: ConventionSchema,
    ) -> FeaturePlan:
        normalized_create = []
        for file_path in plan.files_to_create:
            new_path = file_path
            # Normalize models
            if "model" in file_path.lower():
                models_path = conventions.folder_structure.models_path if conventions.folder_structure else None
                if models_path:
                    if models_path.endswith(".py"):
                        if models_path not in plan.files_to_modify:
                            plan.files_to_modify.append(models_path)
                        continue
                    else:
                        new_path = f"{models_path}/{os.path.basename(file_path)}"
            
            # Normalize routers
            elif "router" in file_path.lower() or "controller" in file_path.lower():
                routers_path = conventions.folder_structure.routers_path if conventions.folder_structure else None
                if routers_path:
                    # Keep module name if it exists
                    parts = file_path.split("/")
                    if len(parts) > 1:
                        new_path = f"{routers_path}/{parts[-2]}/{parts[-1]}"
                    else:
                        new_path = f"{routers_path}/{file_path}"
            
            # Normalize screens
            elif ".dart" in file_path.lower() and "screen" in file_path.lower():
                screens_path = conventions.folder_structure.screens_path if conventions.folder_structure else None
                if screens_path:
                    new_path = f"{screens_path}/{os.path.basename(file_path)}"
                    
            normalized_create.append(new_path)
            
        plan.files_to_create = normalized_create
        
        # Verify no duplicate existing modules
        if conventions.existing_modules:
            for file_path in plan.files_to_create:
                for module in conventions.existing_modules.modules:
                    if module in file_path:
                        raise ValueError(f"Plan attempts to create existing module: {module} in {file_path}. Modify it instead.")
                        
        # Ensure Auth matching
        auth_dep = conventions.auth.dependency_name if conventions.auth else None
        if auth_dep:
            auth_found = any(auth_dep in change for change in plan.backend_changes)
            if not auth_found:
                plan.backend_changes.append(f"Ensure all endpoints are secured with the '{auth_dep}' dependency.")
                
        # Database conventions verification
        base_model = conventions.database.base_model_name if conventions.database else None
        if base_model:
            db_found = any(base_model in change for change in plan.database_changes + plan.backend_changes)
            if not db_found:
                plan.database_changes.append(f"Use the '{base_model}' class for SQLAlchemy models.")

        return plan

    def create_plan(
        self,
        feature_request: str,
        conventions: ConventionSchema,
    ) -> FeaturePlan:
        prompt = self._build_prompt(feature_request, conventions)
        
        import time
        import random
        # MOCK RESPONSE TO AVOID 20 RPD RATE LIMITS
        return FeaturePlan(
            feature_name="Mock Feature",
            description="Mock Feature",
            database_changes=["Mock DB"],
            backend_changes=["Mock API"],
            frontend_changes=["Mock UI"],
            files_to_create=["app/models/mock.py", "app/api/mock.py", "lib/screens/mock.dart"],
            files_to_modify=[],
            dependencies=[],
            risks=[],
            estimated_complexity="low"
        )
