from baer_refqa.audit.metrics import classify_audit, compute_audit_scores

def test_compute_audit_scores_and_classification() -> None:
    scores = compute_audit_scores(
        text_oracle=0.52,
        text_asr=0.31,
        speech_natural=0.68,
        speech_lexicalized=0.42,
    )
    assert round(scores.asr_loss, 2) == 0.21
    assert round(scores.modality_penalty, 2) == -0.16
    assert round(scores.incremental_audio_value, 2) == 0.16
    assert round(scores.prosody_sensitivity, 2) == 0.26
    assert classify_audit(scores) == "audio_essential"
