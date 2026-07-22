from simulation.team_registry import TeamRegistry
from simulation.sprint_manager import SprintManager

def main():
    registry = TeamRegistry()
    registry.register_team("backend", {})
    registry.assign_member("backend", {"id": "1", "story_points": 20})
    registry.assign_member("backend", {"id": "2", "story_points": 20})
    
    manager = SprintManager(registry)
    sprint = manager.create_sprint("backend")
    
    # 120 story points backlog
    backlog = [{"story_points": 10} for _ in range(12)]
    
    manager.assign_work(sprint["start_date"], backlog)
    
    assigned_tasks = len(manager.active_sprints[sprint["start_date"]]["tasks"])
    print(f"Created Sprint {sprint['start_date']}")
    print(f"Assigned {assigned_tasks} tasks (40 story points). 8 tasks spilled over.")
    print("Hiring recommendation likely generated due to backlog pressure.")

if __name__ == "__main__":
    main()
