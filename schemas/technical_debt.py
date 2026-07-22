from pydantic import BaseModel

class TechnicalDebt(BaseModel):
    debt_id: str
    description: str
    module: str
    severity: str
    estimated_cost: int

