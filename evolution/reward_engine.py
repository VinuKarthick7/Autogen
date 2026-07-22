from schemas.engineering_experience import EngineeringExperience
from schemas.reward_signal import RewardSignal

class RewardEngine:
    def compute_reward(self, exp: EngineeringExperience) -> float:
        # formula: + v_success*40 + bench*25 + rep_success*20 - rep_depth*5 - cost*3 - interv*15
        val = 0.0
        val += 40.0 if exp.verification_passed else 0.0
        val += 25.0 * (exp.benchmark_score / 100.0)
        val += 20.0 if exp.repair_success else 0.0
        val -= 5.0 * exp.repair_depth
        val -= 3.0 * exp.cost_usd
        val -= 15.0 if exp.human_intervention else 0.0
        return max(0.0, min(100.0, val)) # Normalize 0-100

    def normalize_reward(self, val: float) -> float:
        return val

    def generate_reward_signal(self, exp: EngineeringExperience) -> RewardSignal:
        total = self.compute_reward(exp)
        return RewardSignal(
            run_id=exp.run_id,
            reward=total,
            verification_reward=40.0 if exp.verification_passed else 0.0,
            benchmark_reward=25.0 * (exp.benchmark_score / 100.0),
            repair_reward=20.0 if exp.repair_success else 0.0,
            efficiency_penalty=3.0 * exp.cost_usd,
            intervention_penalty=15.0 if exp.human_intervention else 0.0
        )
