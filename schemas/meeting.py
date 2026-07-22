from pydantic import BaseModel
from typing import List

class Meeting(BaseModel):
    meeting_id: str
    type: str
    participants: List[str]
    summary: str
    action_items: List[str]

