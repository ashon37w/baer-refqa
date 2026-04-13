from typing import Literal
from pydantic import BaseModel, Field

Track = Literal["track_a_semantic", "track_b_audio"]
TaskType = Literal[
    "semantic_counterfactual",
    "intonation",
    "emotion",
    "pragmatic_intent",
]
Tier = Literal["gold", "silver", "bronze", "reject"]
AuditLabel = Literal[
    "text_sufficient",
    "audio_helpful_not_essential",
    "audio_essential",
    "inconclusive",
]

class GateResult(BaseModel):
    lexical_pass: bool = False
    prosody_pass: bool = False
    auto_label_pass: bool = False
    behavioral_pass: bool = False

class AuditScores(BaseModel):
    asr_loss: float
    modality_penalty: float
    incremental_audio_value: float
    prosody_sensitivity: float
    classification: AuditLabel

class SemanticFamily(BaseModel):
    family_id: str
    source_dataset: str
    source_id: str
    track: Track
    task_type: TaskType
    context: str
    prompt_utterance: str
    question: str
    answer: str
    target_transcript: str
    label_space: list[str] = Field(default_factory=list)

class SampleRecord(BaseModel):
    sample_id: str
    family_id: str
    track: Track
    task_type: TaskType
    question: str
    answer: str
    target_transcript: str
    reference_ids: list[str] = Field(default_factory=list)
    audio_paths: dict[str, str] = Field(default_factory=dict)
    validity: GateResult = Field(default_factory=GateResult)
    audit: AuditScores | None = None
    tier: Tier | None = None
