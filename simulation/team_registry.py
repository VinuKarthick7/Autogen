class TeamRegistry:
    def __init__(self):
        self.teams = {}

    def register_team(self, team_id: str, metadata: dict):
        self.teams[team_id] = {
            "members": [],
            "skills": metadata.get("skills", []),
            "active_story_points": 0,
            "velocity": metadata.get("velocity", 30), # Default historical velocity
            "ownership": metadata.get("ownership", [])
        }

    def assign_member(self, team_id: str, employee: dict):
        if team_id in self.teams:
            self.teams[team_id]["members"].append(employee)

    def remove_member(self, team_id: str, employee_id: str):
        if team_id in self.teams:
            self.teams[team_id]["members"] = [
                m for m in self.teams[team_id]["members"] if m.get("id") != employee_id
            ]

    def find_available_team(self, required_skills: list) -> str:
        for team_id, data in self.teams.items():
            if all(skill in data["skills"] for skill in required_skills):
                # Basic availability check
                if self.compute_capacity(team_id) > 0:
                    return team_id
        return None

    def compute_velocity(self, team_id: str) -> float:
        if team_id in self.teams:
            return self.teams[team_id].get("velocity", 0.0)
        return 0.0

    def compute_capacity(self, team_id: str) -> float:
        if team_id not in self.teams:
            return 0.0
        team = self.teams[team_id]
        # Sum member story points (assume each member contributes 10 points for simplicity)
        total_member_points = sum(m.get("story_points", 10) for m in team["members"])
        return total_member_points - team["active_story_points"]

    def compute_utilization(self, team_id: str) -> float:
        if team_id not in self.teams:
            return 0.0
        team = self.teams[team_id]
        total_member_points = sum(m.get("story_points", 10) for m in team["members"])
        if total_member_points == 0:
            return 0.0
        return min(1.0, team["active_story_points"] / total_member_points)

    def get_team_health(self, team_id: str) -> str:
        utilization = self.compute_utilization(team_id)
        if utilization > 0.9:
            return "Burnout Risk"
        elif utilization < 0.5:
            return "Underutilized"
        return "Healthy"
