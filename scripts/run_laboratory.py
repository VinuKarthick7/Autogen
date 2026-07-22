from laboratory.civilization_metrics import CivilizationMetrics
from laboratory.research_memory import ResearchMemory
from laboratory.evolution_director import EvolutionDirector

def main():
    print("Initializing Autonomous Software Laboratory...")
    memory = ResearchMemory()
    director = EvolutionDirector()
    director.direct_evolution()
    
    metrics = CivilizationMetrics(memory)
    data = metrics.compute_metrics()
    
    print("\nCivilization Metrics:")
    for k, v in data.items():
        print(f"  {k}: {v}")
        
    print(f"\n{metrics.forecast_progress()}")

if __name__ == "__main__":
    main()
