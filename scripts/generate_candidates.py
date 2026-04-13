import json
from pathlib import Path
from baer_refqa.generation.planner import build_generation_jobs
from baer_refqa.reference_bank.models import ReferenceClip
from baer_refqa.schema import SemanticFamily

def main() -> None:
    family = SemanticFamily.model_validate_json(Path("data/interim/one_family.json").read_text(encoding="utf-8"))
    references = [
        ReferenceClip.model_validate_json(line)
        for line in Path("artifacts/reference_bank/reference_bank.jsonl").read_text(encoding="utf-8").splitlines()
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
