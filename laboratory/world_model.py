class WorldModel:
    def __init__(self, memory):
        self.memory = memory
        self.environments = ["Small startup", "SaaS company", "Enterprise", "Government systems", "Offline-first environments", "High-scale systems"]

    def build_world(self, env_type: str) -> dict:
        if env_type not in self.environments:
            env_type = "SaaS company"
        return {"environment": env_type, "constraints": self.simulate_constraints(env_type)}

    def simulate_constraints(self, env_type: str) -> dict:
        if env_type == "Small startup":
            return {"budget": "low", "speed": "high", "scale": "low"}
        elif env_type == "Enterprise":
            return {"budget": "high", "speed": "low", "scale": "high"}
        return {"budget": "medium", "speed": "medium", "scale": "medium"}

    def predict_outcomes(self, world: dict, strategy: str) -> str:
        if world["constraints"]["budget"] == "low" and strategy == "Microservices":
            return "Failure: Too expensive"
        return "Success"
