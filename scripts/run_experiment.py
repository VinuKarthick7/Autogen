from laboratory.research_memory import ResearchMemory
from laboratory.hypothesis_engine import HypothesisEngine
from laboratory.experiment_designer import ExperimentDesigner
from laboratory.strategy_comparator import StrategyComparator

def main():
    memory = ResearchMemory()
    hypo_engine = HypothesisEngine(memory)
    exp_designer = ExperimentDesigner(memory)
    comp = StrategyComparator(memory)

    print("Production incidents increased. Generating hypothesis...")
    hypo = hypo_engine.generate_hypothesis("Repository-specific conventions", {})
    print(f"Hypothesis {hypo['id']}: {hypo['statement']}")

    print("\nDesigning experiment...")
    exp = exp_designer.design_experiment(hypo["id"])
    print(f"Experiment {exp['id']} created: Comparing '{exp['control_group']}' vs '{exp['experimental_group']}'")
    
    print("\nRunning simulated AB test...")
    res = exp_designer.run_ab_test(exp["id"])
    print(f"Result: {res['summary']} (Winner: {res['winner']})")

    if exp_designer.evaluate_significance(res):
        print("=> Better strategy validated and proposed for self-improvement.")
        hypo_engine.retire_hypothesis(hypo["id"])

if __name__ == "__main__":
    main()
