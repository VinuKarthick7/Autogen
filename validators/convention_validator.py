from schemas.generated_file import AgentOutput
from scanners.convention_schema import ConventionSchema

class ConventionValidator:
    def validate(
        self,
        output: AgentOutput,
        conventions: ConventionSchema,
    ) -> dict:
        errors = []
        passed = True

        for file in output.files:
            # 1. Database validation rules
            # We assume database files are Python files that have "sqlalchemy" or "Base" or are located in models_path
            is_database = False
            if file.file_type == "python":
                models_path = conventions.folder_structure.models_path if conventions.folder_structure else None
                if models_path and file.path.startswith(models_path):
                    is_database = True
                elif "sqlalchemy" in file.content or "Mapped[" in file.content:
                    is_database = True
                elif "models" in file.path:
                    is_database = True

            if is_database:
                base_model_name = conventions.database.base_model_name if conventions.database and conventions.database.base_model_name else "Base"
                if base_model_name not in file.content:
                    errors.append("Missing base model")
                
                tenant_field = conventions.database.tenant_field if conventions.database and conventions.database.tenant_field else "tenant_id"
                if tenant_field not in file.content:
                    errors.append("Missing tenant field")
                
                if "Mapped[" not in file.content:
                    errors.append("Missing Mapped typing")
                
                if "mapped_column(" not in file.content:
                    errors.append("Missing mapped_column usage")

            # 2. Backend validation rules
            # We assume backend files include routers
            if file.file_type == "python" and "router" in file.path:
                routers_path = conventions.folder_structure.routers_path if conventions.folder_structure else None
                if routers_path and not file.path.startswith(routers_path):
                    errors.append("Invalid router path")
                
                auth_dep = conventions.auth.dependency_name if conventions.auth else None
                if auth_dep and auth_dep not in file.content:
                    errors.append("Missing auth dependency")

            # 3. Frontend validation rules
            if file.file_type == "dart":
                screens_path = conventions.folder_structure.screens_path if conventions.folder_structure else None
                if screens_path and not file.path.startswith(screens_path):
                    errors.append("Invalid frontend screen path")

        if len(errors) > 0:
            passed = False
            
        return {
            "passed": passed,
            "errors": errors
        }
