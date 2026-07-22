import os
from schemas.generated_file import GeneratedFile
from schemas.patch_operation import PatchOperation

class PatchWriter:
    def __init__(self, workspace_repo_path: str):
        self.workspace_repo_path = workspace_repo_path
        self.restricted_paths = [
            ".env",
            ".git",
            "secrets",
            "config/production",
            "docker-compose.prod.yml"
        ]

    def _is_restricted(self, path: str) -> bool:
        path_lower = path.lower()
        for restricted in self.restricted_paths:
            if restricted in path_lower:
                return True
        return False

    def generate_operation(self, file: GeneratedFile, reason: str = "Agent generated patch") -> PatchOperation:
        if self._is_restricted(file.path):
            raise ValueError(f"Access to restricted path denied: {file.path}")

        full_path = os.path.join(self.workspace_repo_path, file.path)
        
        if os.path.exists(full_path):
            operation = "modify"
            with open(full_path, "r", encoding="utf-8") as f:
                old_content = f.read()
        else:
            operation = "create"
            old_content = None

        return PatchOperation(
            operation=operation,
            path=file.path,
            old_content=old_content,
            new_content=file.content,
            reason=reason
        )

    def apply_operation(self, operation: PatchOperation):
        full_path = os.path.join(self.workspace_repo_path, operation.path)
        
        if operation.operation == "delete":
            if os.path.exists(full_path):
                os.remove(full_path)
        else:
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(operation.new_content)
