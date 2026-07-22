from pydantic import BaseModel

class TopologyGraph(BaseModel):
    nodes: list[str]
    edges: list[dict]
