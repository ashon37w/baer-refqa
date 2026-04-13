import json
from pathlib import Path
from baer_refqa.schema import SampleRecord

def main() -> None:
    target = Path("schemas/refqa_sample.schema.json")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(SampleRecord.model_json_schema(), indent=2),
        encoding="utf-8",
    )
    print(target)

if __name__ == "__main__":
    main()
