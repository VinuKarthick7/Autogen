import os
import json

class ResearchMemory:
    def __init__(self, base_dir="laboratory/memory"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)
        self.files = {
            "hypotheses": os.path.join(self.base_dir, "hypotheses.json"),
            "experiments": os.path.join(self.base_dir, "experiments.json"),
            "strategies": os.path.join(self.base_dir, "strategies.json"),
            "papers": os.path.join(self.base_dir, "papers.json"),
            "predictions": os.path.join(self.base_dir, "predictions.json")
        }
        self._init_files()

    def _init_files(self):
        for path in self.files.values():
            if not os.path.exists(path):
                with open(path, "w") as f:
                    json.dump([], f)

    def _load(self, key: str) -> list:
        if key not in self.files:
            return []
        with open(self.files[key], "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    def _save(self, key: str, data: list):
        if key in self.files:
            with open(self.files[key], "w") as f:
                json.dump(data, f, indent=2)

    def save_hypothesis(self, data: dict):
        items = self._load("hypotheses")
        # Update or append
        for i, item in enumerate(items):
            if item.get("id") == data.get("id"):
                items[i] = data
                self._save("hypotheses", items)
                return
        items.append(data)
        self._save("hypotheses", items)

    def save_experiment(self, data: dict):
        items = self._load("experiments")
        items.append(data)
        self._save("experiments", items)

    def query_history(self, filename: str) -> list:
        # Assuming filename is something like hypotheses.json, map to key
        key = filename.split(".")[0]
        return self._load(key)

    def build_knowledge(self):
        # Build synthesis of history
        return {"status": "knowledge built"}
