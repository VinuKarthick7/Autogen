import uuid

class ScenarioGenerator:
    def __init__(self, memory):
        self.memory = memory
        self.scenarios = ["Scale explosion", "Data corruption", "Economic constraints", "New regulations", "Team turnover", "Vendor lock-in"]

    def generate_scenario(self, category: str) -> dict:
        if category not in self.scenarios:
            category = self.scenarios[0]
            
        return {
            "id": f"SCN-{str(uuid.uuid4())[:8].upper()}",
            "type": category,
            "description": f"Simulating a {category} event."
        }

    def simulate(self, scenario: dict, system_state: dict) -> dict:
        # Mock simulation
        return {"impact": "High", "downtime_minutes": 45}

    def evaluate_resilience(self, simulation_results: dict) -> float:
        downtime = simulation_results.get("downtime_minutes", 0)
        if downtime > 60: return 0.2
        if downtime > 30: return 0.5
        return 0.9
