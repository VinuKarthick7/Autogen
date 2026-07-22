import os
import json

class ArtifactService:
    def __init__(self):
        self.artifacts_dir = "artifacts"
        
    def _get_path(self, run_id: str, filename: str):
        return os.path.join(self.artifacts_dir, run_id, filename)
        
    def load_plan(self, run_id: str):
        with open(self._get_path(run_id, "plan.json"), "r") as f:
            return json.load(f)
            
    def load_chat(self, run_id: str):
        with open(self._get_path(run_id, "chat.json"), "r") as f:
            return json.load(f)
            
    def load_patch(self, run_id: str):
        with open(self._get_path(run_id, "patch.diff"), "r") as f:
            return f.read()
            
    def load_verification(self, run_id: str):
        with open(self._get_path(run_id, "verification_report.json"), "r") as f:
            return json.load(f)
            
    def load_graph(self, run_id: str):
        with open(self._get_path(run_id, "dependency_graph.json"), "r") as f:
            return json.load(f)
            
    def download_artifact(self, run_id: str, filename: str):
        path = self._get_path(run_id, filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Artifact {filename} not found for {run_id}")
        return path
