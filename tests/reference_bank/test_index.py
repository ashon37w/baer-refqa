from baer_refqa.reference_bank.index import rank_references
from baer_refqa.reference_bank.models import ReferenceClip, ReferenceQuery

def test_rank_references_prefers_same_language_and_closest_style() -> None:
    query = ReferenceQuery(
        language="en",
        speaking_rate=4.5,
        pitch_range=110.0,
        terminal_slope=-15.0,
        emotion_hint="questioning",
    )
    clips = [
        ReferenceClip(
            reference_id="bad-lang",
            language="zh",
            speaker_id="spk-1",
            transcript="你好",
            speaking_rate=4.4,
            pitch_range=108.0,
            terminal_slope=-14.0,
            pause_ratio=0.10,
            emotion_hint="questioning",
        ),
        ReferenceClip(
            reference_id="good-match",
            language="en",
            speaker_id="spk-2",
            transcript="Are you sure?",
            speaking_rate=4.6,
            pitch_range=112.0,
            terminal_slope=-16.0,
            pause_ratio=0.11,
            emotion_hint="questioning",
        ),
    ]
    ranked = rank_references(query, clips, top_k=1)
    assert ranked[0].reference_id == "good-match"
