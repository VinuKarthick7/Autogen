from pydantic import BaseModel

class ArchitecturePattern(BaseModel):
    name: str
    description: str
    confidence: float
