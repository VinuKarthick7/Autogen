from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AgentMessage(BaseModel):
    sender: str
    receiver: Optional[str] = None
    message: str
    timestamp: datetime
    metadata: dict = {}
