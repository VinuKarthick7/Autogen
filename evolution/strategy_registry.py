import os
import json
from schemas.strategy_profile import StrategyProfile

class StrategyRegistry:
    def __init__(self, base_dir="evolution/registry"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)
        self.planner_file = os.path.join(self.base_dir, "planner_registry.json")
        self.repair_file = os.path.join(self.base_dir, "repair_registry.json")

    def register_strategy(self, strategy: StrategyProfile):
        pass

    def activate_strategy(self, strategy_id: str):
        pass

    def deprecate_strategy(self, strategy_id: str):
        pass

    def compare_strategies(self, id_a: str, id_b: str):
        pass
