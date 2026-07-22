class VelocityEngine:
    def __init__(self, memory):
        self.memory = memory

    def compute_velocity(self, team_id: str) -> float:
        sprints = self.memory.query_history("sprint_history", lambda s: s.get("team_id") == team_id and s.get("status") == "closed")
        if not sprints:
            return 0.0
        
        recent = sprints[-3:]
        return sum(s.get("delivered_points", 0) for s in recent) / len(recent)

    def forecast_delivery(self, team_id: str, remaining_points: float) -> int:
        velocity = self.compute_velocity(team_id)
        if velocity <= 0:
            return -1
        import math
        return math.ceil(remaining_points / velocity)

    def detect_slowdowns(self, team_id: str) -> float:
        sprints = self.memory.query_history("sprint_history", lambda s: s.get("team_id") == team_id and s.get("status") == "closed")
        if len(sprints) < 2:
            return 0.0
        
        latest = sprints[-1].get("delivered_points", 0)
        previous = sprints[-2].get("delivered_points", 0)
        if previous == 0:
            return 0.0
        
        # Negative means slowdown
        return (latest - previous) / previous

    def predict_burnout(self, team_id: str) -> float:
        slowdown = self.detect_slowdowns(team_id)
        # simplistic burnout predictor based on sustained slowdowns
        if slowdown <= -0.3:
            return 0.85 # High risk
        elif slowdown < 0:
            return 0.4
        return 0.1
