from pydantic import BaseModel

class Recommendation(BaseModel):
    recommendation_id: str
    category: str
    title: str
    description: str
    expected_improvement: float
    confidence: float
