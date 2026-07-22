from pydantic import BaseModel

class PerformanceReport(BaseModel):
    report_id: str
    average_latency_ms: float
    p95_latency_ms: float
    throughput: float
    cpu_usage: float
    memory_usage: float
    bottlenecks: list[str]
