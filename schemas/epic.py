from pydantic import BaseModel

class Epic(BaseModel):
    epic_id: str
    title: str
    description: str
    business_value: str
    stories: list[str]
    dependencies: list[str]
    estimated_points: int
