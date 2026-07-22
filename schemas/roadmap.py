from pydantic import BaseModel

class Roadmap(BaseModel):
    roadmap_id: str
    product_name: str
    milestones: list[str]
    releases: list[str]
    risks: list[str]
    timeline_weeks: int
