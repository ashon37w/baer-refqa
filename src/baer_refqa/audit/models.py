from typing import Literal
from pydantic import BaseModel

ConditionName = Literal[
    "text_oracle",
    "text_asr",
    "speech_natural",
    "speech_lexicalized",
    "speech_revoiced",
]

class ConditionObservation(BaseModel):
    sample_id: str
    task_slice: str
    condition: ConditionName
    correct: float
