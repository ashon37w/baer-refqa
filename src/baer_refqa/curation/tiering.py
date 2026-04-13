from baer_refqa.schema import SampleRecord


def decide_tier(sample: SampleRecord) -> str:
    validity = sample.validity
    if not validity.lexical_pass:
        return "reject"
    if sample.audit is None or sample.audit.classification == "inconclusive":
        return "bronze"
    all_gates = (
        validity.lexical_pass
        and validity.prosody_pass
        and validity.auto_label_pass
        and validity.behavioral_pass
    )
    if sample.track == "track_b_audio":
        if all_gates and sample.audit.classification == "audio_essential":
            return "gold"
        if validity.prosody_pass and validity.auto_label_pass:
            return "silver"
        return "bronze"
    if all_gates:
        return "gold"
    if validity.prosody_pass and validity.auto_label_pass:
        return "silver"
    return "bronze"
