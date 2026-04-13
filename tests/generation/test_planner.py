from baer_refqa.generation.planner import build_generation_jobs
from baer_refqa.reference_bank.models import ReferenceClip
from baer_refqa.schema import SemanticFamily

def test_build_generation_jobs_expands_family_over_references_and_modes() -> None:
    family = SemanticFamily(
        family_id="ifqa::42",
        source_dataset="ifqa",
        source_id="42",
        track="track_b_audio",
        task_type="pragmatic_intent",
        context="The listener is annoyed.",
        prompt_utterance="You are coming.",
        question="Which pragmatic force best matches the utterance?",
        answer="challenge",
        target_transcript="You are coming.",
        label_space=["request", "challenge", "confirmation"],
    )
    references = [
        ReferenceClip(
            reference_id="ref-1",
            language="en",
            speaker_id="spk-1",
            transcript="Are you sure?",
            speaking_rate=4.2,
            pitch_range=98.0,
            terminal_slope=-14.0,
            pause_ratio=0.08,
            emotion_hint="questioning",
        ),
        ReferenceClip(
            reference_id="ref-2",
            language="en",
            speaker_id="spk-2",
            transcript="Come in now.",
            speaking_rate=4.8,
            pitch_range=120.0,
            terminal_slope=-8.0,
            pause_ratio=0.05,
            emotion_hint="challenging",
        ),
    ]
    jobs = build_generation_jobs(family, references, modes=("zero_shot", "revoice"))
    assert len(jobs) == 4
    assert {job.generation_mode for job in jobs} == {"zero_shot", "revoice"}
