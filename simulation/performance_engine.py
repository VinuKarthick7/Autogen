class PerformanceEngine:
    def __init__(self, velocity_engine, team_registry):
        self.velocity_engine = velocity_engine
        self.team_registry = team_registry

    def evaluate_team(self, team_id: str) -> float:
        velocity = self.velocity_engine.compute_velocity(team_id)
        burnout = self.velocity_engine.predict_burnout(team_id)
        
        morale = max(0.0, 1.0 - burnout)
        reliability = 0.9 # Mock
        blocked_tasks = 0.1 # Mock percentage of tasks blocked
        
        # Normalize velocity (assume 50 is a good baseline)
        normalized_velocity = min(1.0, velocity / 50.0)
        
        team_health = (0.30 * normalized_velocity) + (0.20 * morale) + (0.20 * reliability) - (0.15 * burnout) - (0.15 * blocked_tasks)
        return max(0.0, min(1.0, team_health))

    def generate_metrics(self, team_id: str) -> dict:
        return {
            "health_score": self.evaluate_team(team_id),
            "burnout_risk": self.velocity_engine.predict_burnout(team_id),
            "morale": max(0.0, 1.0 - self.velocity_engine.predict_burnout(team_id)),
            "reliability": 0.9,
            "pressure": self.team_registry.compute_utilization(team_id)
        }

    def generate_health_report(self, team_id: str) -> dict:
        metrics = self.generate_metrics(team_id)
        status = "Healthy"
        if metrics["health_score"] < 0.4:
            status = "Critical Risk"
        elif metrics["health_score"] < 0.7:
            status = "Warning"
            
        return {
            "team_id": team_id,
            "status": status,
            "metrics": metrics
        }
