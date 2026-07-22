class ArchitectureBoard:
    def __init__(self, memory):
        self.memory = memory
        self.members = ["ArchitectAgent", "TechLeadAgent", "SREAgent", "ProductManagerAgent"]

    def review_rfc(self, rfc_id: str) -> dict:
        rfcs = self.memory.load_history("rfcs")
        rfc = next((r for r in rfcs if r.get("id") == rfc_id), None)
        if not rfc:
            return {"error": "RFC not found"}
        
        # Mock review process
        score = self.score_design(rfc)
        votes = self.collect_votes(rfc)
        
        approved = votes["approve"] > votes["reject"]
        if approved:
            return self.approve_design(rfc_id, score)
        else:
            if score < 50:
                return self.reject_design(rfc_id, "Score too low")
            else:
                return self.request_changes(rfc_id, "Need to address SRE concerns")

    def score_design(self, rfc: dict) -> float:
        # Placeholder deterministic scoring based on lengths
        complexity = min(100, len(rfc.get("architecture", [])) * 10)
        scalability = 80 # Assumed
        security = 90
        reliability = 85
        maintainability = max(0, 100 - complexity)
        cost = min(100, len(rfc.get("alternatives", [])) * 20)
        
        # Weighted average
        return (complexity*0.1 + scalability*0.2 + security*0.2 + reliability*0.2 + maintainability*0.2 + (100-cost)*0.1)

    def collect_votes(self, rfc: dict) -> dict:
        # Mock votes
        return {"approve": 3, "reject": 1}

    def approve_design(self, rfc_id: str, score: float):
        from simulation.rfc_engine import RFCEngine
        engine = RFCEngine(self.memory)
        return engine.evaluate_rfc(rfc_id, f"Approved with score {score}", "Approved")

    def reject_design(self, rfc_id: str, reason: str):
        from simulation.rfc_engine import RFCEngine
        engine = RFCEngine(self.memory)
        return engine.evaluate_rfc(rfc_id, reason, "Rejected")

    def request_changes(self, rfc_id: str, feedback: str):
        from simulation.rfc_engine import RFCEngine
        engine = RFCEngine(self.memory)
        return engine.evaluate_rfc(rfc_id, feedback, "Needs Changes")
