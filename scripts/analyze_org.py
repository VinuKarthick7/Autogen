from simulation.team_registry import TeamRegistry
from simulation.velocity_engine import VelocityEngine
from simulation.organization_memory import OrganizationMemory
from simulation.performance_engine import PerformanceEngine
import uuid

def main():
    print("Analyzing Organization Health...")
    
    memory = OrganizationMemory()
    # Mocking some negative sprint history to show velocity drop
    s1 = {"sprint_id": "1", "team_id": "backend", "status": "closed", "delivered_points": 40}
    s2 = {"sprint_id": "2", "team_id": "backend", "status": "closed", "delivered_points": 28} # 30% drop
    memory.save_sprint(s1)
    memory.save_sprint(s2)
    
    registry = TeamRegistry()
    registry.register_team("backend", {})
    velocity = VelocityEngine(memory)
    performance = PerformanceEngine(velocity, registry)
    
    drop = velocity.detect_slowdowns("backend")
    burnout = velocity.predict_burnout("backend")
    
    print(f"\nTeam: backend")
    print(f"Velocity Trend: {drop*100:.1f}%")
    
    if drop <= -0.3:
        print("=> Burnout Warning! Velocity dropped by >= 30%.")
        print("=> Hiring Recommendation Generated.")

if __name__ == "__main__":
    main()
