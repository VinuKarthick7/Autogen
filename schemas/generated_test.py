from pydantic import BaseModel
from typing import Literal

class GeneratedTest(BaseModel):
    test_id: str
    module: str
    test_type: Literal[
        "unit",
        "integration",
        "e2e",
        "property",
        "load"
    ]
    test_code: str
    coverage_score: float
    priority: str
