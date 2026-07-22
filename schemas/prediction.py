from pydantic import BaseModel

class Prediction(BaseModel):
    id: str
    metric: str
    predicted_value: float
    timeframe_days: int
    confidence: float
