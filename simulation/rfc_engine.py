import uuid
import datetime

class RFCEngine:
    def __init__(self, memory):
        self.memory = memory

    def generate_rfc(self, title: str, problem: str, architecture: list, alternatives: list, risks: list) -> dict:
        rfc = {
            "id": f"RFC-{str(uuid.uuid4())[:8].upper()}",
            "title": title,
            "problem": problem,
            "architecture": architecture,
            "alternatives": alternatives,
            "risks": risks,
            "status": "Pending review",
            "created_at": datetime.datetime.now().isoformat()
        }
        self.memory.save_rfc(rfc)
        return rfc

    def evaluate_rfc(self, rfc_id: str, feedback: str, new_status: str):
        rfcs = self.memory.load_history("rfcs")
        for rfc in rfcs:
            if rfc["id"] == rfc_id:
                rfc["status"] = new_status
                rfc["latest_feedback"] = feedback
                self.memory.save_rfc(rfc)
                return rfc
        return None

    def publish_rfc(self, rfc_id: str):
        return self.evaluate_rfc(rfc_id, "Approved by board", "Published")

    def archive_rfc(self, rfc_id: str):
        return self.evaluate_rfc(rfc_id, "Archived", "Archived")
