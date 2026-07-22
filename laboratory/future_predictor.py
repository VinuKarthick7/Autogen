import uuid
import datetime

class FuturePredictor:
    def __init__(self, memory):
        self.memory = memory

    def predict(self, metric: str, current_value: float, trend: float, days_into_future: int) -> dict:
        predicted = current_value + (trend * days_into_future)
        prediction = {
            "id": f"PRD-{str(uuid.uuid4())[:8].upper()}",
            "metric": metric,
            "predicted_value": predicted,
            "timeframe_days": days_into_future,
            "confidence": self.estimate_confidence(days_into_future),
            "created_at": datetime.datetime.now().isoformat()
        }
        return prediction

    def estimate_confidence(self, days_into_future: int) -> float:
        # Confidence drops as timeframe increases
        return max(0.1, 1.0 - (days_into_future / 365.0))

    def generate_warnings(self, predictions: list) -> list:
        warnings = []
        for p in predictions:
            if p["metric"] == "technical_debt" and p["predicted_value"] > 100:
                warnings.append(f"Warning: Technical debt predicted to exceed safe threshold in {p['timeframe_days']} days.")
        return warnings
