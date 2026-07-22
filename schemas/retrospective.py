from pydantic import BaseModel
from typing import List

class Retrospective(BaseModel):
    retrospective_id: str
    sprint_id: str
    what_went_well: List[str]
    what_failed: List[str]
    action_items: List[str]

