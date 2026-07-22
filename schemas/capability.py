from pydantic import BaseModel

class Capability(BaseModel):
    id: str
    name: str
    description: str
    maturity_level: float
