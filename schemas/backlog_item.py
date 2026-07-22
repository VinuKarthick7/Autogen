from pydantic import BaseModel

class BacklogItem(BaseModel):
    item_id: str
    title: str
    description: str
    epic_id: str
    story_points: int
    owner_team: str | None
    dependencies: list[str]
    priority: str

