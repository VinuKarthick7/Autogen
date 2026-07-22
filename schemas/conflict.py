from pydantic import BaseModel

class Conflict(BaseModel):
    conflict_id: str
    topic: str
    participants: list[str]
    viewpoints: dict[str, str]
    resolution: str | None

