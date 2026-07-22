class HiringEngine:
    def __init__(self, team_registry, backlog_manager, velocity_engine):
        self.team_registry = team_registry
        self.backlog_manager = backlog_manager
        self.velocity_engine = velocity_engine

    def analyze_gaps(self, team_id: str) -> dict:
        capacity = self.team_registry.compute_capacity(team_id)
        pressure = self.backlog_manager.compute_backlog_pressure(capacity)
        velocity_trend = self.velocity_engine.detect_slowdowns(team_id)
        
        return {
            "pressure": pressure,
            "velocity_declining": velocity_trend < 0
        }

    def recommend_hires(self, team_id: str) -> dict:
        gaps = self.analyze_gaps(team_id)
        
        # IF backlog_pressure > 0.8 AND velocity declining THEN recommend hiring.
        if gaps["pressure"] > 0.8 and gaps["velocity_declining"]:
            return {
                "team_id": team_id,
                "problem": "Backend bottleneck detected",
                "recommendation": "Hire 2 Senior Engineers",
                "confidence": 0.88,
                "metrics": gaps
            }
        return None

    def forecast_capacity(self, team_id: str, new_hires: int) -> float:
        current_cap = self.team_registry.compute_capacity(team_id)
        # Assume each new hire brings 10 story points capacity
        return current_cap + (new_hires * 10)

    def estimate_roi(self, new_capacity: float, backlog_pressure: float) -> float:
        # Simple heuristic
        if new_capacity <= 0:
            return 0.0
        new_pressure = backlog_pressure / new_capacity
        return backlog_pressure - new_pressure # ROI is pressure reduction
