class QualityService:
    def evaluate(self, repository: str) -> dict:
        return {
            "security_score": 0.95,
            "performance_score": 0.88,
            "reliability_score": 0.99
        }
