import os
import subprocess
import time
from typing import Optional

class TestRunner:
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
        if framework == "flutter":
            cmd = ["flutter", "test"]
        elif framework == "node":
            cmd = ["npm", "test"]
        elif framework == "python":
            cmd = ["python", "-m", "pytest"]
        else:
            return True, 0, "No test framework detected.", ""

        start_time = time.time()
        try:
            result = subprocess.run(cmd, cwd=self.workspace_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            success = result.returncode == 0
            stdout = result.stdout
            stderr = result.stderr
        except FileNotFoundError:
            success = False
            stdout = ""
            stderr = f"Command not found: {cmd[0]}"
            
        duration_ms = int((time.time() - start_time) * 1000)
        return success, duration_ms, stdout, stderr
