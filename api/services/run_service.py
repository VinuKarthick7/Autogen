import os
import json
import uuid
from datetime import datetime
from api.schemas.run_status import RunStatus
from api.schemas.create_run import CreateRunRequest

class RunService:
    def __init__(self):
        self.storage_dir = os.path.join("storage", "runs")
        os.makedirs(self.storage_dir, exist_ok=True)
        
    def _get_run_dir(self, run_id: str) -> str:
        return os.path.join(self.storage_dir, run_id)
        
    def create_run(self, request: CreateRunRequest) -> RunStatus:
        run_id = str(uuid.uuid4())
        run_dir = self._get_run_dir(run_id)
        os.makedirs(run_dir, exist_ok=True)
        
        status = RunStatus(
            run_id=run_id,
            status="queued",
            current_stage="queued",
            progress=0,
            repair_depth=0,
            verification_passed=False,
            created_at=datetime.utcnow()
        )
        
        with open(os.path.join(run_dir, "metadata.json"), "w") as f:
            f.write(request.model_dump_json())
            
        self.update_status(run_id, status)
        return status
        
    def update_status(self, run_id: str, status: RunStatus):
        run_dir = self._get_run_dir(run_id)
        with open(os.path.join(run_dir, "status.json"), "w") as f:
            f.write(status.model_dump_json())
            
    def get_status(self, run_id: str) -> RunStatus:
        run_dir = self._get_run_dir(run_id)
        path = os.path.join(run_dir, "status.json")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Run {run_id} not found")
        with open(path, "r") as f:
            return RunStatus.model_validate_json(f.read())
            
    def list_runs(self) -> list[RunStatus]:
        runs = []
        for d in os.listdir(self.storage_dir):
            try:
                runs.append(self.get_status(d))
            except Exception:
                pass
        return sorted(runs, key=lambda x: x.created_at, reverse=True)
