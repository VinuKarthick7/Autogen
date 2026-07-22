import uuid

class HypothesisEngine:
    def __init__(self, memory):
        self.memory = memory

    def generate_hypothesis(self, topic: str, context: dict) -> dict:
        hypo = {
            "id": f"HYP-{str(uuid.uuid4())[:8].upper()}",
            "statement": f"Implementing {topic} will improve reliability by 15%",
            "confidence": 0.83,
            "status": "Active",
            "proposed_by": "System"
        }
        self.memory.save_hypothesis(hypo)
        return hypo

    def rank_hypotheses(self) -> list:
        hypos = self.memory.query_history("hypotheses.json")
        return sorted(hypos, key=lambda x: x.get("confidence", 0), reverse=True)

    def retire_hypothesis(self, hyp_id: str):
        hypos = self.memory.query_history("hypotheses.json")
        for h in hypos:
            if h["id"] == hyp_id:
                h["status"] = "Retired"
                self.memory.save_hypothesis(h)

    def estimate_impact(self, hyp_id: str) -> float:
        return 0.9 # Mock
