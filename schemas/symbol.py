from dataclasses import dataclass
from typing import Literal

@dataclass
class Symbol:
    name: str
    type: Literal["class", "function", "router", "model", "schema", "service", "unknown"]
    file_path: str
