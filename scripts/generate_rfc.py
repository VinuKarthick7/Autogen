from simulation.organization_memory import OrganizationMemory
from simulation.rfc_engine import RFCEngine
from simulation.architecture_board import ArchitectureBoard
from simulation.conflict_resolver import ConflictResolver

def main():
    memory = OrganizationMemory()
    engine = RFCEngine(memory)
    board = ArchitectureBoard(memory)
    resolver = ConflictResolver(memory)
    
    print("Generating RFC...")
    rfc = engine.generate_rfc("Offline Booking", "Properties lose internet connectivity.", ["Queue", "Sync Service"], ["Kafka", "PostgreSQL outbox"], [])
    print(f"Created {rfc['id']}")
    
    print("\nArchitect proposes Kafka. SRE rejects (Operational burden).")
    resolution = resolver.resolve_conflict("DB Choice", ["PostgreSQL outbox", "Kafka"], "cost optimization")
    print(f"Conflict Resolved. Decision: {resolution['decision']}")
    
    # Update RFC with decision
    engine.evaluate_rfc(rfc['id'], f"Board decided: {resolution['decision']}", "Approved")
    print("RFC Updated and Approved.")

if __name__ == "__main__":
    main()
