from typing import List
from pydantic import BaseModel


class SolveRequest(BaseModel):
    code: str
    language: str
    save: bool = False


class MatchSubmitRequest(BaseModel):
    code: str
    language: str
