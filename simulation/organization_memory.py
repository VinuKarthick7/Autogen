import os
import json

class OrganizationMemory:
    def __init__(self, base_dir="simulation/memory"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)
        self.files = {
            "rfcs": os.path.join(self.base_dir, "rfcs.json"),
            "retrospectives": os.path.join(self.base_dir, "retrospectives.json"),
            "decisions": os.path.join(self.base_dir, "decisions.json"),
            "meetings": os.path.join(self.base_dir, "meetings.json"),
            "sprint_history": os.path.join(self.base_dir, "sprint_history.json"),
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

    def save_rfc(self, rfc_data: dict):
        rfcs = self._load("rfcs")
        # Update if exists, else append
        for i, existing in enumerate(rfcs):
            if existing.get("id") == rfc_data.get("id"):
                rfcs[i] = rfc_data
                self._save("rfcs", rfcs)
                return
        rfcs.append(rfc_data)
        self._save("rfcs", rfcs)

    def save_sprint(self, sprint_data: dict):
        sprints = self._load("sprint_history")
        sprints.append(sprint_data)
        self._save("sprint_history", sprints)

    def save_retrospective(self, retro_data: dict):
        retros = self._load("retrospectives")
        retros.append(retro_data)
        self._save("retrospectives", retros)

    def save_meeting(self, meeting_data: dict):
        meetings = self._load("meetings")
        meetings.append(meeting_data)
        self._save("meetings", meetings)

    def load_history(self, key: str) -> list:
        return self._load(key)

    def query_history(self, key: str, filter_func) -> list:
        data = self._load(key)
        return [item for item in data if filter_func(item)]
