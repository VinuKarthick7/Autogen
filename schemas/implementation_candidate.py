from pydantic import BaseModel

class ImplementationCandidate(BaseModel):
    repository: str
    file_path: str
    symbol_name: str
    code_snippet: str
    similarity_score: float
