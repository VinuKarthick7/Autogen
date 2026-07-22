class TechnologyEvaluator:
    def __init__(self, memory):
        self.memory = memory

    def evaluate_stack(self, stack: list) -> dict:
        return {tech: self.compute_scores(tech) for tech in stack}

    def compute_scores(self, tech: str) -> dict:
        # Mock scores
        return {
            "Complexity": 5,
            "Cost": 3,
            "Reliability": 8,
            "Performance": 9,
            "Operational burden": 4
        }

    def recommend_stack(self, requirements: dict) -> list:
        return ["PostgreSQL", "FastAPI", "Redis"]
