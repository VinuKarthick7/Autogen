from pydantic import BaseModel

class AcceptanceTest(BaseModel):
    test_id: str
    story_id: str
    scenario: str
    given: str
    when: str
    then: str
    passed: bool
