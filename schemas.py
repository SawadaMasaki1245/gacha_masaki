from pydantic import BaseModel
from typing import List

class GachaResult(BaseModel):
    result: str
    count: int

class GachaTenResults(BaseModel):
    results: List[str]
    count: int