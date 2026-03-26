from pydantic import BaseModel
from typing import List

class Email(BaseModel):
    text: str
    emotion: str
    priority: str

class Observation(BaseModel):
    emails: List[dict]
    overwhelm_score: float

class Action(BaseModel):
    emotion: str
    priority: str
    decision: str  # reply / ignore / schedule

class Reward(BaseModel):
    score: float