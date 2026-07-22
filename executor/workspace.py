import os
import shutil
import uuid
import logging

logger = logging.getLogger(__name__)

class WorkspaceManager:
    def __init__(self, base_dir: str = "workspaces"):
        self.base_dir = base_dir

    def create_workspace(self, run_id: str) -> str:
        workspace_path = os.path.join(self.base_dir, f"run_{run_id}")
        os.makedirs(workspace_path, exist_ok=True)
        return workspace_path

    def copy_repository(self, source_repo: str, target_repo: str):
        if not os.path.exists(source_repo):
            raise FileNotFoundError(f"Source repository {source_repo} does not exist.")
            
        if os.path.exists(target_repo):
            shutil.rmtree(target_repo)
            
        # We use shutil.copytree but ignore .git to re-init it cleanly later
        # OR we just copy everything including .git if we want to retain history.
        # Let's copy everything except maybe __pycache__ and .pytest_cache.
        shutil.copytree(
            source_repo, 
            target_repo, 
            ignore=shutil.ignore_patterns('__pycache__', '.pytest_cache', '*.pyc', '.git')
        )
        logger.info(f"Copied repository from {source_repo} to {target_repo}")

    def cleanup_workspace(self, run_id: str):
        workspace_path = os.path.join(self.base_dir, f"run_{run_id}")
        if os.path.exists(workspace_path):
            shutil.rmtree(workspace_path, ignore_errors=True)
            logger.info(f"Cleaned up workspace {workspace_path}")
