from pydantic import BaseModel

class TestSuite(BaseModel):
    suite_id: str
    name: str
    tests: list[str]
    coverage_score: float
