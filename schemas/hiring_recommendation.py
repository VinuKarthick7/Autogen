from pydantic import BaseModel

class HiringRecommendation(BaseModel):
    recommendation_id: str
    team_id: str
    role: str
    reason: str

