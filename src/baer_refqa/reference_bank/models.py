from pydantic import BaseModel

class ReferenceClip(BaseModel):
    reference_id: str
    language: str
    speaker_id: str
    transcript: str
    speaking_rate: float
    pitch_range: float
    terminal_slope: float
    pause_ratio: float
    emotion_hint: str | None = None

class ReferenceQuery(BaseModel):
    language: str
    speaking_rate: float
    pitch_range: float
    terminal_slope: float
    emotion_hint: str | None = None
