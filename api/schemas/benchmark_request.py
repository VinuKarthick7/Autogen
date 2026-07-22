from pydantic import BaseModel
from typing import Optional

class BenchmarkRequest(BaseModel):
    suite: str
    difficulty: Optional[str] = None
