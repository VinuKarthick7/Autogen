from pydantic import BaseModel

class BenchmarkRun(BaseModel):
    id: str
    architecture: str
    throughput: float
    latency: float
    cost: float
