from pydantic import BaseModel
from typing import Literal

class ProductRequirement(BaseModel):
    requirement_id: str
    title: str
    description: str
    stakeholders: list[str]
    business_goal: str
    functional_requirements: list[str]
    non_functional_requirements: list[str]
    constraints: list[str]
    assumptions: list[str]
    priority: Literal[
        "critical",
        "high",
        "medium",
        "low"
    ]
