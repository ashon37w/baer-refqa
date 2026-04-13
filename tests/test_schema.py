import pytest
from pydantic import ValidationError
from baer_refqa.schema import SampleRecord

def test_sample_record_accepts_known_tracks_only() -> None:
    record = SampleRecord(
        sample_id="sample-1",
        family_id="ifqa::1",
        track="track_b_audio",
        task_type="pragmatic_intent",
        question="Which pragmatic force is most likely?",
        answer="request",
        target_transcript="You are coming.",
    )
    assert record.track == "track_b_audio"

    with pytest.raises(ValidationError):
        SampleRecord(
            sample_id="sample-2",
            family_id="ifqa::2",
            track="router",
            task_type="semantic_counterfactual",
            question="Where is the tower?",
            answer="Berlin",
            target_transcript="Where is the tower?",
        )
