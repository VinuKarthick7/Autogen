from pydantic import BaseModel
from typing import Optional

class ApprovalRequest(BaseModel):
    notes: Optional[str] = None
