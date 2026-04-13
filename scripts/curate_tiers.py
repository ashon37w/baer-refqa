import json
from pathlib import Path
from baer_refqa.curation.tiering import decide_tier
from baer_refqa.schema import SampleRecord


def main() -> None:
    source = Path("artifacts/audit/enriched_samples.jsonl")
    target = Path("artifacts/audit/tiered_samples.jsonl")
    target.parent.mkdir(parents=True, exist_ok=True)
    with source.open("r", encoding="utf-8") as reader, target.open("w", encoding="utf-8") as writer:
        for line in reader:
            sample = SampleRecord.model_validate_json(line)
            sample.tier = decide_tier(sample)
            writer.write(json.dumps(sample.model_dump(), ensure_ascii=False) + "\n")
    print(target)


if __name__ == "__main__":
    main()
