from pydantic import BaseModel

class ExecutionResult(BaseModel):
    run_id: str
    branch_name: str
    files_changed: int
    diff_path: str
    committed: bool
    rollback_available: bool
    verification_passed: bool = True
