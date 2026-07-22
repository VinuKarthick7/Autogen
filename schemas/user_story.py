from pydantic import BaseModel

class UserStory(BaseModel):
    story_id: str
    title: str
    description: str
    persona: str
    acceptance_criteria: list[str]
    technical_dependencies: list[str]
    estimated_points: int
    priority: str
