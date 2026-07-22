from schemas.patch_set import PatchSet

class SafetyChecker:
    def __init__(self):
        self.restricted_terms = [
            "alembic",
            "migrations",
            ".github/workflows",
            "gitlab-ci",
            "jenkins",
            "scanners/",
            "schemas/",
            "tests/", # might allow tests eventually, but for now reject core test overrides? The user only said "modifying CI/CD, overwriting scanner code"
        ]

    def _is_restricted(self, path: str) -> bool:
        path_lower = path.lower()
        
        if "alembic" in path_lower or "migrations" in path_lower:
            return True
        if ".github" in path_lower or "ci.yml" in path_lower or "gitlab" in path_lower:
            return True
        if "scanners/" in path_lower:
            return True
            
        return False

    def validate_patch(self, patch_set: PatchSet):
        for operation in patch_set.operations:
            if operation.operation == "delete" and "core" in operation.path.lower():
                raise ValueError(f"Safety Violation: Cannot delete core files ({operation.path})")
                
            if self._is_restricted(operation.path):
                raise ValueError(f"Safety Violation: Path is restricted ({operation.path})")
                
            if "secret" in operation.path.lower() or "password" in operation.path.lower():
                raise ValueError(f"Safety Violation: Cannot modify secrets ({operation.path})")
