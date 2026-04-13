from baer_refqa.schema import AuditScores

def compute_audit_scores(
    *,
    text_oracle: float,
    text_asr: float,
    speech_natural: float,
    speech_lexicalized: float,
) -> AuditScores:
    asr_loss = text_oracle - text_asr
    modality_penalty = text_oracle - speech_natural
    incremental_audio_value = speech_natural - text_oracle
    prosody_sensitivity = speech_natural - speech_lexicalized
    return AuditScores(
        asr_loss=asr_loss,
        modality_penalty=modality_penalty,
        incremental_audio_value=incremental_audio_value,
        prosody_sensitivity=prosody_sensitivity,
        classification=classify_audit_values(
            modality_penalty=modality_penalty,
            incremental_audio_value=incremental_audio_value,
            prosody_sensitivity=prosody_sensitivity,
        ),
    )

def classify_audit_values(
    *,
    modality_penalty: float,
    incremental_audio_value: float,
    prosody_sensitivity: float,
    iav_eps: float = 0.02,
    ps_eps: float = 0.02,
    max_modality_penalty: float = 0.20,
) -> str:
    if modality_penalty > max_modality_penalty:
        return "inconclusive"
    if incremental_audio_value > iav_eps and prosody_sensitivity > ps_eps:
        return "audio_essential"
    if abs(incremental_audio_value) <= iav_eps and abs(prosody_sensitivity) <= ps_eps:
        return "text_sufficient"
    return "audio_helpful_not_essential"

def classify_audit(scores: AuditScores) -> str:
    return scores.classification
