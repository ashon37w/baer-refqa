from baer_refqa.curation.tiering import decide_tier
from baer_refqa.schema import AuditScores, GateResult, SampleRecord


def test_track_b_gold_requires_audio_essential_and_all_gates() -> None:
    sample = SampleRecord(
        sample_id="sample-1",
        family_id="ifqa::42",
        track="track_b_audio",
        task_type="pragmatic_intent",
        question="Which pragmatic force best matches the utterance?",
        answer="challenge",
        target_transcript="You are coming.",
        validity=GateResult(
            lexical_pass=True,
            prosody_pass=True,
            auto_label_pass=True,
            behavioral_pass=True,
        ),
        audit=AuditScores(
            asr_loss=0.10,
            modality_penalty=0.01,
            incremental_audio_value=0.11,
            prosody_sensitivity=0.09,
            classification="audio_essential",
        ),
    )
    assert decide_tier(sample) == "gold"


def test_track_b_silver_requires_prosody_and_auto_pass() -> None:
    sample = SampleRecord(
        sample_id="sample-2",
        family_id="ifqa::43",
        track="track_b_audio",
        task_type="pragmatic_intent",
        question="Which pragmatic force best matches the utterance?",
        answer="challenge",
        target_transcript="You are coming.",
        validity=GateResult(
            lexical_pass=True,
            prosody_pass=True,
            auto_label_pass=True,
            behavioral_pass=False,
        ),
        audit=AuditScores(
            asr_loss=0.10,
            modality_penalty=0.01,
            incremental_audio_value=0.11,
            prosody_sensitivity=0.09,
            classification="audio_helpful_not_essential",
        ),
    )
    assert decide_tier(sample) == "silver"


def test_reject_when_lexical_fails() -> None:
    sample = SampleRecord(
        sample_id="sample-3",
        family_id="ifqa::44",
        track="track_b_audio",
        task_type="pragmatic_intent",
        question="Which pragmatic force best matches the utterance?",
        answer="challenge",
        target_transcript="You are coming.",
        validity=GateResult(
            lexical_pass=False,
            prosody_pass=True,
            auto_label_pass=True,
            behavioral_pass=True,
        ),
        audit=AuditScores(
            asr_loss=0.10,
            modality_penalty=0.01,
            incremental_audio_value=0.11,
            prosody_sensitivity=0.09,
            classification="audio_essential",
        ),
    )
    assert decide_tier(sample) == "reject"


def test_bronze_when_inconclusive() -> None:
    sample = SampleRecord(
        sample_id="sample-4",
        family_id="ifqa::45",
        track="track_a_semantic",
        task_type="semantic_counterfactual",
        question="Which meaning matches the utterance?",
        answer="meaning_a",
        target_transcript="The sky is blue.",
        validity=GateResult(
            lexical_pass=True,
            prosody_pass=True,
            auto_label_pass=True,
            behavioral_pass=True,
        ),
        audit=AuditScores(
            asr_loss=0.10,
            modality_penalty=0.01,
            incremental_audio_value=0.11,
            prosody_sensitivity=0.09,
            classification="inconclusive",
        ),
    )
    assert decide_tier(sample) == "bronze"


def test_track_a_gold_requires_all_gates() -> None:
    sample = SampleRecord(
        sample_id="sample-5",
        family_id="ifqa::46",
        track="track_a_semantic",
        task_type="semantic_counterfactual",
        question="Which meaning matches the utterance?",
        answer="meaning_a",
        target_transcript="The sky is blue.",
        validity=GateResult(
            lexical_pass=True,
            prosody_pass=True,
            auto_label_pass=True,
            behavioral_pass=True,
        ),
        audit=AuditScores(
            asr_loss=0.10,
            modality_penalty=0.01,
            incremental_audio_value=0.11,
            prosody_sensitivity=0.09,
            classification="text_sufficient",
        ),
    )
    assert decide_tier(sample) == "gold"


def test_track_b_bronze_fallback() -> None:
    sample = SampleRecord(
        sample_id="sample-6",
        family_id="ifqa::47",
        track="track_b_audio",
        task_type="pragmatic_intent",
        question="Which pragmatic force best matches the utterance?",
        answer="challenge",
        target_transcript="You are coming.",
        validity=GateResult(
            lexical_pass=True,
            prosody_pass=False,
            auto_label_pass=False,
            behavioral_pass=False,
        ),
        audit=AuditScores(
            asr_loss=0.10,
            modality_penalty=0.01,
            incremental_audio_value=0.11,
            prosody_sensitivity=0.09,
            classification="audio_essential",
        ),
    )
    assert decide_tier(sample) == "bronze"


def test_audit_none_is_bronze() -> None:
    sample = SampleRecord(
        sample_id="sample-7",
        family_id="ifqa::48",
        track="track_a_semantic",
        task_type="semantic_counterfactual",
        question="Which meaning matches the utterance?",
        answer="meaning_a",
        target_transcript="The sky is blue.",
        validity=GateResult(
            lexical_pass=True,
            prosody_pass=True,
            auto_label_pass=True,
            behavioral_pass=True,
        ),
        audit=None,
    )
    assert decide_tier(sample) == "bronze"
