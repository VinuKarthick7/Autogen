from pydantic import BaseModel
from typing import List

class ResearchPaper(BaseModel):
    id: str
    title: str
    abstract: str
    findings: List[str]
    authors: List[str]
