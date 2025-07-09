from typing import Literal
from dataclasses import dataclass

@dataclass
class Prize:
    rank: Literal["S", "A", "B", "C"]
    rate: float