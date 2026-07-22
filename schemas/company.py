from pydantic import BaseModel
from typing import List

class Company(BaseModel):
    company_id: str
    name: str
    ceo_id: str
    departments: List[str]

