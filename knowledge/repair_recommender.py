from schemas.repair_pattern import RepairPattern

class RepairRecommender:
    def __init__(self):
        # Mocking existing history
        self.history = [
            RepairPattern(
                pattern_id="rp-1",
                category="MissingImport",
                repositories=["pms", "erp"],
                trigger="NameError",
                repair_strategy="Add import statement at top of file",
                success_rate=0.94,
                average_repair_depth=1.1
            )
        ]

    def recommend_repairs(self, failure_category: str) -> list[dict]:
        recommendations = []
        for h in self.history:
            if h.category == failure_category:
                recommendations.append({
                    "repair": h.repair_strategy,
                    "success_rate": h.success_rate
                })
        return recommendations

    def rank_repairs(self, recommendations: list[dict]) -> list[dict]:
        return sorted(recommendations, key=lambda x: x["success_rate"], reverse=True)

    def learn_from_repair(self, repair_data: dict):
        pass
