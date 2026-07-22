from pathlib import Path

from scanners.convention_schema import (
    ApiConvention,
    AuthConvention,
    ConventionSchema,
    DatabaseConvention,
    ExistingModules,
    FolderStructure,
    FrontendConvention,
    ProjectInfo,
)


class PythonConventionScanner:
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)

    def folder_exists(self, relative_path: str) -> bool:
        return (self.project_root / relative_path).exists()

    def detect_backend_framework(self) -> str:
        main_file = self.project_root / "app" / "main.py"

        if main_file.exists():
            content = main_file.read_text(
                encoding="utf-8",
                errors="ignore",
            )

            if "FastAPI(" in content:
                return "FastAPI"

        return "Unknown"

    def detect_database(self) -> str:
        if self.folder_exists("alembic"):
            return "PostgreSQL"

        return "Unknown"

    def detect_modules(self) -> list[str]:
        modules_dir = self.project_root / "app" / "modules"

        if not modules_dir.exists():
            return []

        ignore_set = {
            "__pycache__",
            ".git",
            ".idea",
            ".vscode",
        }

        return sorted(
            [
                item.name
                for item in modules_dir.iterdir()
                if item.is_dir() and item.name not in ignore_set and not item.name.startswith(".")
            ]
        )

    def detect_auth(self) -> AuthConvention:
        auth = AuthConvention()

        files_to_scan = [
            self.project_root / "app" / "core" / "security.py",
        ]

        deps_dir = self.project_root / "app" / "core"

        if deps_dir.exists():
            files_to_scan.extend(deps_dir.rglob("*.py"))

        for file in files_to_scan:
            if not file.exists():
                continue

            content = file.read_text(
                encoding="utf-8",
                errors="ignore",
            )

            if "OAuth2PasswordBearer" in content:
                auth.auth_type = "JWT"

            if "get_current_user" in content:
                auth.dependency_name = "get_current_user"

            if "require_role" in content or "get_current_role" in content:
                auth.role_checker = "require_role"

        return auth

    def detect_database_conventions(self) -> DatabaseConvention:
        db_conv = DatabaseConvention(
            migration_tool="Alembic" if self.folder_exists("alembic") else None
        )

        files_to_scan = []
        
        # Standard models path
        models_dir = self.project_root / "app" / "models"
        if models_dir.exists():
            files_to_scan.extend(models_dir.rglob("*.py"))
            
        core_db = self.project_root / "app" / "core" / "database.py"
        if core_db.exists():
            files_to_scan.append(core_db)

        # Fallback to infra for this specific structure
        infra_models_dir = self.project_root / "app" / "infra" / "models"
        if infra_models_dir.exists():
            files_to_scan.extend(infra_models_dir.rglob("*.py"))
            
        infra_models_file = self.project_root / "app" / "infra" / "models.py"
        if infra_models_file.exists():
            files_to_scan.append(infra_models_file)
            
        infra_db = self.project_root / "app" / "infra" / "database.py"
        if infra_db.exists():
            files_to_scan.append(infra_db)

        all_content = ""
        for file in files_to_scan:
            if file.exists():
                all_content += file.read_text(encoding="utf-8", errors="ignore") + "\n"

        if "class Base(" in all_content or "Base = declarative_base(" in all_content:
            db_conv.base_model_name = "Base"

        expected_common = ["id", "created_at", "updated_at", "tenant_id", "property_id", "user_id"]
        found_common = []
        for field in expected_common:
            if f"{field}:" in all_content or f"{field} =" in all_content or f"{field}=" in all_content:
                found_common.append(field)
                
        db_conv.common_fields = sorted(list(set(found_common)))

        expected_timestamps = ["created_at", "updated_at", "deleted_at"]
        found_timestamps = []
        for field in expected_timestamps:
            if f"{field}:" in all_content or f"{field} =" in all_content or f"{field}=" in all_content:
                found_timestamps.append(field)
                
        db_conv.timestamp_fields = sorted(list(set(found_timestamps)))

        expected_tenants = ["tenant_id", "property_id", "organization_id"]
        for field in expected_tenants:
            if f"{field}:" in all_content or f"{field} =" in all_content or f"{field}=" in all_content:
                db_conv.tenant_field = field
                break

        return db_conv

    def scan(self) -> ConventionSchema:
        return ConventionSchema(
            project_info=ProjectInfo(
                name=self.project_root.name,
                backend_framework=self.detect_backend_framework(),
                frontend_framework="Unknown",
                database=self.detect_database(),
            ),
            folder_structure=FolderStructure(
                routers_path="app/modules",
                models_path="app/models",
                services_path="app/services",
            ),
            database=self.detect_database_conventions(),
            auth=self.detect_auth(),
            api=ApiConvention(),
            frontend=FrontendConvention(),
            existing_modules=ExistingModules(
                modules=self.detect_modules()
            ),
        )