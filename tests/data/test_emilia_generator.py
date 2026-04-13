from baer_refqa.data.emilia_generator import generate_emilia_batch
from baer_refqa.reference_bank.models import ReferenceClip

def test_generate_emilia_batch_produces_valid_clips():
    clips = generate_emilia_batch(n=10, seed=7)
    assert len(clips) == 10
    for clip in clips:
        ref = ReferenceClip.model_validate(clip)
        assert ref.language == "en"
        assert 0 < ref.speaking_rate < 10
        assert ref.reference_id.startswith("emilia-ref-")

def test_emilia_batch_is_deterministic():
    batch1 = generate_emilia_batch(n=5, seed=42)
    batch2 = generate_emilia_batch(n=5, seed=42)
    assert batch1 == batch2
