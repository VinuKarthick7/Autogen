import os
import subprocess
import logging

logger = logging.getLogger(__name__)

class GitManager:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path

    def _run_cmd(self, cmd: list[str]) -> str:
        result = subprocess.run(
            cmd,
            cwd=self.repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            raise RuntimeError(f"Git command failed: {' '.join(cmd)}\nStdout: {result.stdout}\nStderr: {result.stderr}")
        return result.stdout.strip()

    def initialize(self):
        self._run_cmd(["git", "init"])
        self._run_cmd(["git", "config", "user.name", "AI Agent"])
        self._run_cmd(["git", "config", "user.email", "agent@pinesphere.com"])
        self._run_cmd(["git", "add", "."])
        try:
            self._run_cmd(["git", "commit", "-m", "Initial commit"])
        except RuntimeError as e:
            # If there's nothing to commit, that's fine
            if "nothing to commit" not in str(e):
                raise

    def create_branch(self, run_id: str):
        branch_name = f"agent/run_{run_id}"
        self._run_cmd(["git", "checkout", "-b", branch_name])
        return branch_name

    def commit(self, message: str):
        self._run_cmd(["git", "add", "."])
        self._run_cmd(["git", "commit", "-m", message])

    def rollback(self):
        self._run_cmd(["git", "reset", "--hard", "HEAD"])
        self._run_cmd(["git", "clean", "-fd"])

    def get_diff(self) -> str:
        # Get diff of working tree vs HEAD
        # Also need to get diff of newly added but untracked files? 
        # Better yet, add everything to index then diff --cached, or just add and diff HEAD.
        self._run_cmd(["git", "add", "."])
        try:
            diff = self._run_cmd(["git", "diff", "--cached"])
        except RuntimeError:
            diff = ""
        # Unstage so we don't automatically commit if we just wanted diff
        self._run_cmd(["git", "reset"])
        return diff

    def get_status(self) -> str:
        return self._run_cmd(["git", "status", "-s"])
