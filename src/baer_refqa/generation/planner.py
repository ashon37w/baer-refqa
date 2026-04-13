from baer_refqa.generation.models import GenerationJob
from baer_refqa.reference_bank.models import ReferenceClip
from baer_refqa.schema import SemanticFamily

def build_generation_jobs(
    family: SemanticFamily,
    references: list[ReferenceClip],
    modes: tuple[str, ...] = ("zero_shot", "revoice"),
) -> list[GenerationJob]:
    jobs: list[GenerationJob] = []
    for reference in references:
        for mode in modes:
            jobs.append(
                GenerationJob(
                    job_id=f"{family.family_id}::{reference.reference_id}::{mode}",
                    family_id=family.family_id,
                    reference_id=reference.reference_id,
                    generation_mode=mode,
                    transcript=family.target_transcript,
                    output_path=f"artifacts/generation/{family.family_id}__{reference.reference_id}__{mode}.wav",
                )
            )
    return jobs
