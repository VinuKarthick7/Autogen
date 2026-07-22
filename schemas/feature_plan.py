from pydantic import BaseModel
from typing import Literal

class FeaturePlan(BaseModel):
    feature_name: str
    description: str
    database_changes: list[str]
    backend_changes: list[str]
    frontend_changes: list[str]
    files_to_create: list[str]
    files_to_modify: list[str]
    dependencies: list[str]
    risks: list[str]
    estimated_complexity: Literal["low", "medium", "high"]
