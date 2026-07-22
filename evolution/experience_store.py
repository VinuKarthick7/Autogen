import os
import json
from schemas.engineering_experience import EngineeringExperience
from schemas.prompt_version import PromptVersion
from datetime import datetime

class ExperienceStore:
    def __init__(self, base_dir="evolution/experiences"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)
        self.exp_file = os.path.join(self.base_dir, "experiences.jsonl")

    def store_experience(self, exp: EngineeringExperience):
        with open(self.exp_file, "a") as f:
            f.write(exp.model_dump_json() + "\n")

    def get_experience(self, run_id: str):
        experiences = self.query_experiences()
        for e in experiences:
            if e.run_id == run_id:
                return e
        return None

    def query_experiences(self) -> list[EngineeringExperience]:
        exps = []
        if os.path.exists(self.exp_file):
            with open(self.exp_file, "r") as f:
                for line in f:
                    if line.strip():
                        exps.append(EngineeringExperience(**json.loads(line)))
        return exps

    def get_repository_history(self, repo_id: str) -> list[EngineeringExperience]:
        return [e for e in self.query_experiences() if e.repository_id == repo_id]

    def get_strategy_history(self, strategy: str) -> list[EngineeringExperience]:
        return [e for e in self.query_experiences() if e.planner_version == strategy or e.repair_strategy == strategy]
