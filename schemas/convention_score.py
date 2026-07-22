from pydantic import BaseModel

class ConventionScore(BaseModel):
    structure: float
    auth: float
    database: float
    api: float
    services: float
    total_score: float
