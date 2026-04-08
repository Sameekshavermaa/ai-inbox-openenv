from pydantic import BaseModel, field_validator
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

    @field_validator("score")
    def clamp_score(cls, v):
        return max(0.05, min(0.95, v))
