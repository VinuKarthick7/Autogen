from pydantic import BaseModel
from typing import Literal

class RFC(BaseModel):
    rfc_id: str
    title: str
    author: str
    architecture: str
    alternatives: list[str]
    risks: list[str]
    status: Literal['draft', 'review', 'approved', 'rejected']

