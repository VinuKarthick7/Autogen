import uuid
import datetime

class ConflictResolver:
    def __init__(self, memory):
        self.memory = memory

    def detect_conflict(self, opinions: list) -> bool:
        # Simplistic: if opinions differ, there's a conflict
        if not opinions:
            return False
        first_opinion = opinions[0].get("stance")
        return any(o.get("stance") != first_opinion for o in opinions)

    def collect_opinions(self, topic: str) -> list:
        # Mock opinions
        return [
            {"role": "Architect", "stance": "Use Kafka", "weight": 1.5},
            {"role": "Backend", "stance": "Too expensive", "weight": 1.0},
            {"role": "SRE", "stance": "Operational burden", "weight": 1.2}
        ]

    def score_options(self, options: list, strategy="reliability optimization") -> str:
        # Deterministic resolution for simulation purposes
        if strategy == "cost optimization":
            return "Use PostgreSQL outbox."
        elif strategy == "reliability optimization":
            return "Use Kafka."
        else:
            return options[0] if options else "No decision"

    def resolve_conflict(self, topic: str, options: list, strategy="cost optimization") -> dict:
        opinions = self.collect_opinions(topic)
        if not self.detect_conflict(opinions):
            decision = options[0] if options else "No conflict"
        else:
            decision = self.score_options(options, strategy)
            
        resolution = {
            "id": f"RES-{str(uuid.uuid4())[:8].upper()}",
            "topic": topic,
            "decision": decision,
            "strategy": strategy,
            "timestamp": datetime.datetime.now().isoformat()
        }
        self.store_resolution(resolution)
        return resolution

    def store_resolution(self, resolution: dict):
        self.memory.save_meeting(resolution)
