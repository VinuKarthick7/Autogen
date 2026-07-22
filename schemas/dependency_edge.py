from dataclasses import dataclass

@dataclass
class DependencyEdge:
    source: str
    target: str
    relation_type: str = "imports"
