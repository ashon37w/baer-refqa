import json
from pathlib import Path
from baer_refqa.generation.planner import build_generation_jobs
from baer_refqa.reference_bank.models import ReferenceClip
from baer_refqa.schema import SemanticFamily
from baer_refqa.settings import Settings

def main() -> None:
    settings = Settings(repo_root=Path(__file__).resolve().parents[1])
    # Read first family from semantic_families.jsonl
    families_path = settings.interim_dir / "semantic_families.jsonl"
    families = [
        json.loads(l) for l in families_path.read_text(encoding="utf-8").splitlines() if l.strip()
    ]
    family = SemanticFamily.model_validate(families[0])
    # Read reference clips from emilia_metadata.jsonl
    references = [
        ReferenceClip.model_validate_json(line)
        for line in (settings.raw_dir / "emilia_metadata.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    jobs = build_generation_jobs(family, references[:3])
    target = Path("artifacts/generation/generation_jobs.jsonl")
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as handle:
        for job in jobs:
            handle.write(json.dumps(job.model_dump(), ensure_ascii=False) + "\n")
    print(target)

if __name__ == "__main__":
    main()
