from pydantic import BaseModel

class OrganizationalMetric(BaseModel):
    metric_id: str
    name: str
    value: float
    timestamp: str

