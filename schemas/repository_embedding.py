from pydantic import BaseModel

class RepositoryEmbedding(BaseModel):
    repo_id: str
    embedding_model: str
    vector: list[float]
    dimensions: int
