from typing import List
from pydantic import BaseModel


class SolveRequest(BaseModel):
    code: str
    language: str
    save: bool = False


class SubmitBatchRequest(BaseModel):
    results: List[dict]  # { passed: bool, error: str }
