from pydantic import BaseModel

class RuntimeSummary(BaseModel):
    telemetry_events: int
    incidents_detected: int
    root_cause_accuracy: float
    sla_violations: int
    automatic_rollbacks: int
    cost_savings_percent: float
    average_mttr_minutes: float
