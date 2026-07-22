class ArchitectureExplorer:
    def __init__(self, memory):
        self.memory = memory

    def generate_architectures(self) -> list:
        return ["Monolith", "Modular monolith", "Microservices", "Event-driven systems", "CQRS", "Event sourcing"]

    def evaluate_tradeoffs(self, architecture: str) -> dict:
        # Mock evaluation
        return {
            "architecture": architecture,
            "complexity": "high" if architecture in ["Microservices", "CQRS", "Event sourcing"] else "low",
            "scalability": "high" if architecture in ["Microservices", "Event-driven systems"] else "medium"
        }

    def recommend_architecture(self, context: dict) -> str:
        if context.get("scale") == "high":
            return "Microservices"
        return "Modular monolith"
