from simulation.organization_memory import OrganizationMemory
from simulation.retrospective_engine import RetrospectiveEngine

def main():
    memory = OrganizationMemory()
    retro_engine = RetrospectiveEngine(memory)
    
    print("Sprint ended. Running Retrospective...")
    retro = retro_engine.generate_retrospective("SPRINT-123", velocity_trend=-0.2, burnout_risk=0.8)
    
    print("\nRetrospective Generated:")
    print("What failed:")
    for f in retro["what_failed"]:
        print(f"  - {f}")
        
    print("Action items:")
    for a in retro["action_items"]:
        print(f"  - {a}")
        
    print("\nLessons stored in Organization Memory.")

if __name__ == "__main__":
    main()
