from pydantic import BaseModel

class AuditEvent(BaseModel):
    event_id: str
    category: str
    description: str
    timestamp: str
