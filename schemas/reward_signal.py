from pydantic import BaseModel

class RewardSignal(BaseModel):
    run_id: str
    reward: float
    verification_reward: float
    benchmark_reward: float
    repair_reward: float
    efficiency_penalty: float
    intervention_penalty: float
