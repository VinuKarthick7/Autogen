import os
import subprocess
import time
from typing import Optional

class LintRunner:
    def __init__(self, workspace_path: str):
        self.workspace_path = workspace_path

    def detect_framework(self) -> Optional[str]:
        if os.path.exists(os.path.join(self.workspace_path, "pubspec.yaml")):
            return "flutter"
        elif os.path.exists(os.path.join(self.workspace_path, "package.json")):
            return "node"
        elif os.path.exists(os.path.join(self.workspace_path, "pytest.ini")) or any(f.endswith(".py") for f in os.listdir(self.workspace_path)):
            return "python"
        return None

    def run(self) -> tuple[bool, int, str, str]:
        framework = self.detect_framework()
        cmds = []
        if framework == "flutter":
            cmds.append(["flutter", "analyze"])
        elif framework == "node":
            cmds.append(["npm", "run", "lint"])
        elif framework == "python":
            cmds.append(["python", "-m", "ruff", "check", "."])
            cmds.append(["python", "-m", "mypy", "."])
        else:
            return True, 0, "No lint framework detected.", ""

        start_time = time.time()
        success = True
        stdout = ""
        stderr = ""
        
        for cmd in cmds:
            try:
                result = subprocess.run(cmd, cwd=self.workspace_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                stdout += f"--- {cmd[0]} ---\n{result.stdout}\n"
                stderr += result.stderr
                if result.returncode != 0:
                    success = False
            except FileNotFoundError:
                success = False
                stderr += f"Command not found: {cmd[0]}\n"
            
        duration_ms = int((time.time() - start_time) * 1000)
        return success, duration_ms, stdout, stderr
