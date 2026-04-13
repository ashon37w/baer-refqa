from baer_refqa.schema import AuditScores


def passes_behavioral_validity(
    audit: AuditScores,
    *,
    require_audio_essential: bool,
) -> bool:
    if audit.classification == "inconclusive":
        return False
    if require_audio_essential:
        return audit.classification == "audio_essential"
    return audit.classification in {
        "text_sufficient",
        "audio_helpful_not_essential",
        "audio_essential",
    }
