from pydantic import BaseModel

class Assignment(BaseModel):
    assignment_id: str
    item_id: str
    assignee_id: str
    status: str

