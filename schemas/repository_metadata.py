from pydantic import BaseModel
from datetime import datetime

class RepositoryMetadata(BaseModel):
    repo_id: str
    name: str
    path: str
    language: str
    framework: str
    database: str
    architecture_style: str
    modules: list[str]
    conventions: dict
    indexed_at: datetime
