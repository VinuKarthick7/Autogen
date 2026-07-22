from pydantic import BaseModel

class ChaosResult(BaseModel):
    experiment_id: str
    scenario: str
    service_affected: str
    recovery_time_ms: int
    data_loss: bool
    passed: bool
