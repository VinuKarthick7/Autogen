from pydantic import BaseModel

class ReleasePlan(BaseModel):
    release_id: str
    name: str
    target_date: str
    features: list[str]
