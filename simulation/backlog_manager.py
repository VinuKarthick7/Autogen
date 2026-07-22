class BacklogManager:
    def __init__(self):
        self.items = []

    def add_item(self, item: dict):
        self.items.append(item)

    def prioritize_backlog(self, strategy="RICE"):
        if strategy == "RICE":
            # Reach * Impact * Confidence / Effort
            def rice_score(item):
                reach = item.get("reach", 1)
                impact = item.get("impact", 1)
                confidence = item.get("confidence", 1.0)
                effort = item.get("effort", 1)
                if effort == 0: effort = 1
                return (reach * impact * confidence) / effort
            
            self.items.sort(key=rice_score, reverse=True)
            
        elif strategy == "WSJF":
            # Cost of Delay / Job Size
            def wsjf_score(item):
                cod = item.get("business_value", 1) + item.get("time_criticality", 1) + item.get("risk_reduction", 1)
                size = item.get("effort", 1)
                if size == 0: size = 1
                return cod / size
                
            self.items.sort(key=wsjf_score, reverse=True)
            
        elif strategy == "MoSCoW":
            priorities = {"Must": 4, "Should": 3, "Could": 2, "Won't": 1}
            self.items.sort(key=lambda x: priorities.get(x.get("moscow", "Could"), 0), reverse=True)

    def estimate_work(self):
        # Naive automated estimation based on word count
        for item in self.items:
            if "story_points" not in item:
                words = len(item.get("description", "").split())
                if words < 10: item["story_points"] = 1
                elif words < 30: item["story_points"] = 3
                elif words < 100: item["story_points"] = 5
                else: item["story_points"] = 8

    def rank_dependencies(self):
        # Sort items so that items with 0 dependencies come first
        self.items.sort(key=lambda x: len(x.get("dependencies", [])))

    def compute_backlog_pressure(self, team_capacity: float) -> float:
        if team_capacity <= 0:
            return float('inf')
        total_points = sum(item.get("story_points", 0) for item in self.items if item.get("status") != "done")
        return total_points / team_capacity

    def detect_bottbottlenecks(self):
        # Find items that block many other items
        blockers = {}
        for item in self.items:
            for dep in item.get("dependencies", []):
                blockers[dep] = blockers.get(dep, 0) + 1
        return sorted(blockers.items(), key=lambda x: x[1], reverse=True)
