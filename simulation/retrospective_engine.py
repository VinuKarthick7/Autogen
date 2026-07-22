import uuid
import datetime

class RetrospectiveEngine:
    def __init__(self, memory):
        self.memory = memory

    def generate_retrospective(self, sprint_id: str, velocity_trend: float, burnout_risk: float) -> dict:
        retro = {
            "id": f"RET-{str(uuid.uuid4())[:8].upper()}",
            "sprint_id": sprint_id,
            "date": datetime.datetime.now().isoformat(),
            "what_went_well": [],
            "what_failed": [],
            "action_items": []
        }
        
        # Analyze and generate lessons based on metrics
        if velocity_trend > 0:
            retro["what_went_well"].append("Velocity increased over previous sprint.")
        elif velocity_trend < 0:
            retro["what_failed"].append("Velocity dropped significantly.")
            retro["action_items"].append("Investigate blockers and tech debt.")
            
        if burnout_risk > 0.5:
            retro["what_failed"].append("Team is overloaded.")
            retro["action_items"].append("Hire more engineers or reduce sprint scope.")
            
        self.memory.save_retrospective(retro)
        return retro

    def extract_lessons(self, retro_id: str):
        retros = self.memory.load_history("retrospectives")
        retro = next((r for r in retros if r.get("id") == retro_id), None)
        if not retro:
            return []
        
        return retro.get("what_failed", []) + retro.get("what_went_well", [])

    def track_actions(self, retro_id: str):
        retros = self.memory.load_history("retrospectives")
        retro = next((r for r in retros if r.get("id") == retro_id), None)
        return retro.get("action_items", []) if retro else []

    def score_team_learning(self, team_id: str) -> float:
        # Mock: count number of action items resolved (assumed 50% for simulation)
        return 0.5
