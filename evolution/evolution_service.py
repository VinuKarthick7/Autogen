from evolution.recommendation_engine import RecommendationEngine
from evolution.experiment_manager import ExperimentManager
from evolution.learning_pipeline import LearningPipeline

class EvolutionService:
    def __init__(self):
        self.recommendation_engine = RecommendationEngine()
        self.experiment_manager = ExperimentManager()
        self.learning_pipeline = LearningPipeline()

    def trigger_learning_cycle(self):
        return self.learning_pipeline.run_learning_cycle()

    def get_recommendations(self):
        return self.recommendation_engine.generate_recommendations()

    def get_strategy_rankings(self):
        return [
            {"rank": 1, "strategy": "Planner V13", "success": 0.91, "cost": 0.45, "runtime": 12.4},
            {"rank": 2, "strategy": "Planner V12", "success": 0.84, "cost": 0.50, "runtime": 15.2}
        ]

    def get_experiments(self):
        return self.experiment_manager.get_experiments()

    def get_prompt_history(self):
        return []
