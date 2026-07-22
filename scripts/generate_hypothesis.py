from laboratory.research_memory import ResearchMemory
from laboratory.hypothesis_engine import HypothesisEngine

def main():
    memory = ResearchMemory()
    engine = HypothesisEngine(memory)
    hypo = engine.generate_hypothesis("Graph retrieval planning", {})
    print(f"New Hypothesis Generated: {hypo['id']}")
    print(f"Statement: {hypo['statement']}")
    print(f"Confidence: {hypo['confidence']}")

if __name__ == "__main__":
    main()
