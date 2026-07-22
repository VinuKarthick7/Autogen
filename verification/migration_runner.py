import os
import subprocess
import time

class MigrationRunner:
    def __init__(self, workspace_path: str):
        self.workspace_path = workspace_path

    def has_migrations(self) -> bool:
        return os.path.exists(os.path.join(self.workspace_path, "alembic")) or \
               os.path.exists(os.path.join(self.workspace_path, "migrations")) or \
               os.path.exists(os.path.join(self.workspace_path, "alembic.ini"))

    def run(self) -> tuple[bool, int, str, str]:
        if not self.has_migrations():
            return True, 0, "No migrations detected.", ""

        start_time = time.time()
        cmd = ["alembic", "upgrade", "head"]
        
        try:
            result = subprocess.run(cmd, cwd=self.workspace_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            success = result.returncode == 0
            stdout = result.stdout
            stderr = result.stderr
            
            if success:
                # Rollback to verify downgrade works
                rb_result = subprocess.run(["alembic", "downgrade", "-1"], cwd=self.workspace_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdout += "\n--- Rollback ---\n" + rb_result.stdout
                stderr += rb_result.stderr
                if rb_result.returncode != 0:
                    success = False
        except FileNotFoundError:
            success = False
            stdout = ""
            stderr = f"Command not found: alembic"
            
        duration_ms = int((time.time() - start_time) * 1000)
        return success, duration_ms, stdout, stderr
