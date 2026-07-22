from pydantic import BaseModel

class CrossRepoMatch(BaseModel):
    source_repo: str
    target_repo: str
    similarity_score: float
    matching_modules: list[str]
    matching_patterns: list[str]
