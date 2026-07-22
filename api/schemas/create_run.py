from pydantic import BaseModel
from typing import Optional

class CreateRunRequest(BaseModel):
    repository_path: str
    feature_request: str
    branch_name: Optional[str] = None
    benchmark_mode: bool = False
    auto_approve: bool = False
    mock_mode: bool = False
