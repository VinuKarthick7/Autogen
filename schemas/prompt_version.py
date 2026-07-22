from pydantic import BaseModel
from datetime import datetime

class PromptVersion(BaseModel):
    prompt_id: str
    agent_type: str
    version: str
    prompt_text: str
    success_rate: float
    average_score: float
    average_cost: float
    created_at: datetime
