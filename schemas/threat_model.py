from pydantic import BaseModel

class ThreatModel(BaseModel):
    model_id: str
    service: str
    assets: list[str]
    trust_boundaries: list[str]
    attack_vectors: list[str]
    mitigations: list[str]
