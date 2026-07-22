from pydantic import BaseModel
from typing import Optional

class RuleViolation(BaseModel):
    severity: str
    category: str
    file: str
    line: int
    message: str
    suggestion: str
