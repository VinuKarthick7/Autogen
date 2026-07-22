from typing import Literal, Optional
from pydantic import BaseModel

class PatchOperation(BaseModel):
    operation: Literal["create", "modify", "delete"]
    path: str
    old_content: Optional[str] = None
    new_content: str
    reason: str
