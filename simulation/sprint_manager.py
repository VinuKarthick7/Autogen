from simulation.team_registry import TeamRegistry
import uuid
import datetime

class SprintManager:
    def __init__(self, team_registry: TeamRegistry):
        self.team_registry = team_registry
        self.active_sprints = {}

    def create_sprint(self, team_id: str, duration_days: int = 14) -> dict:
        sprint_id = str(uuid.uuid4())
        self.active_sprints[sprint_id] = {
            "team_id": team_id,
            "tasks": [],
            "start_date": datetime.datetime.now().isoformat(),
            "end_date": (datetime.datetime.now() + datetime.timedelta(days=duration_days)).isoformat(),
            "status": "active"
        }
        return self.active_sprints[sprint_id]

    def assign_work(self, sprint_id: str, backlog: list):
        if sprint_id not in self.active_sprints:
            return
            
        sprint = self.active_sprints[sprint_id]
        team_id = sprint["team_id"]
        team_capacity = self.team_registry.compute_capacity(team_id)
        
        assigned_points = 0
        for item in backlog:
            item_points = item.get("story_points", 0)
            if item.get("status") == "blocked":
                continue # Rollover blocked stories
            
            # Team cannot exceed capacity
            if assigned_points + item_points <= team_capacity:
                sprint["tasks"].append(item)
                assigned_points += item_points
                # For simplicity, tech debt consumes capacity implicitly by taking up story points
            else:
                break # Capacity reached

        self.team_registry.teams[team_id]["active_story_points"] = assigned_points

    def close_sprint(self, sprint_id: str) -> dict:
        if sprint_id not in self.active_sprints:
            return None
        sprint = self.active_sprints[sprint_id]
        sprint["status"] = "closed"
        
        team_id = sprint["team_id"]
        # Free up capacity
        self.team_registry.teams[team_id]["active_story_points"] = 0
        
        # Calculate delivered points (assume all non-blocked completed)
        delivered = sum(t.get("story_points", 0) for t in sprint["tasks"] if t.get("status") != "blocked")
        sprint["delivered_points"] = delivered
        
        return sprint

    def calculate_burndown(self, sprint_id: str) -> list:
        # Mock burndown: linear decrease over sprint
        if sprint_id not in self.active_sprints:
            return []
        sprint = self.active_sprints[sprint_id]
        total_points = sum(t.get("story_points", 0) for t in sprint["tasks"])
        # Return daily points remaining
        return [{"day": i, "remaining": max(0, total_points - (total_points/14)*i)} for i in range(15)]

    def compute_velocity(self, team_id: str, historical_sprints: list) -> float:
        team_sprints = [s for s in historical_sprints if s.get("team_id") == team_id and s.get("status") == "closed"]
        if not team_sprints:
            return self.team_registry.compute_velocity(team_id)
        
        total_delivered = sum(s.get("delivered_points", 0) for s in team_sprints[-3:]) # Average of last 3
        return total_delivered / min(len(team_sprints), 3)

    def forecast_completion(self, total_backlog_points: int, team_velocity: float) -> int:
        if team_velocity <= 0:
            return -1 # Infinite
        import math
        return math.ceil(total_backlog_points / team_velocity)
