from pydantic import BaseModel

class Dependency(BaseModel):
    dependency_id: str
    dependent_item: str
    blocking_item: str
    dependency_type: str
