from pydantic import BaseModel
from typing import Literal, List

class BenchmarkCase(BaseModel):
    id: str
    repository_type: str
    difficulty: Literal["easy", "medium", "hard", "expert"]
    category: str = "general"
    feature_request: str
    expected_modules: List[str]
    expected_files: List[str]
    expected_dependencies: List[str]
    expected_repairs: List[str]
    max_repair_depth: int
    tags: List[str]
