import pytest
from laboratory.hypothesis_engine import HypothesisEngine
from laboratory.experiment_designer import ExperimentDesigner
from laboratory.strategy_comparator import StrategyComparator
from laboratory.world_model import WorldModel
from laboratory.scenario_generator import ScenarioGenerator
from laboratory.future_predictor import FuturePredictor
from laboratory.research_memory import ResearchMemory

def test_hypothesis_engine():
    memory = ResearchMemory()
    engine = HypothesisEngine(memory)
    hypo = engine.generate_hypothesis("Graph Retrieval", {})
    assert "Graph Retrieval" in hypo["statement"]
    assert hypo["status"] == "Active"

def test_experiment_designer():
    memory = ResearchMemory()
    designer = ExperimentDesigner(memory)
    exp = designer.design_experiment("HYP-123")
    assert exp["hypothesis_id"] == "HYP-123"
    assert exp["status"] == "Designed"

def test_strategy_comparator():
    memory = ResearchMemory()
    comp = StrategyComparator(memory)
    res = comp.compare_strategies("A", "B", ["Latency"])
    winner = comp.compute_winner(res)
    assert winner in ["strategy_a", "strategy_b"]

def test_world_model():
    memory = ResearchMemory()
    world = WorldModel(memory)
    env = world.build_world("Small startup")
    assert env["constraints"]["budget"] == "low"

def test_scenario_generator():
    memory = ResearchMemory()
    gen = ScenarioGenerator(memory)
    scn = gen.generate_scenario("Data corruption")
    assert scn["type"] == "Data corruption"

def test_future_predictor():
    memory = ResearchMemory()
    predictor = FuturePredictor(memory)
    pred = predictor.predict("technical_debt", 50, 1.5, 60)
    assert pred["predicted_value"] == 50 + (1.5 * 60)
    assert pred["timeframe_days"] == 60
