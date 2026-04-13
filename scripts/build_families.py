import json
from pathlib import Path
from baer_refqa.text.family_builder import build_semantic_family

def main() -> None:
    source = Path("data/raw/source_rows.jsonl")
    target = Path("data/interim/semantic_families.jsonl")
    target.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    with source.open("r", encoding="utf-8") as handle:
        for line in handle:
            raw = json.loads(line)
            rows.append(build_semantic_family(raw).model_dump())
    with target.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(target)

if __name__ == "__main__":
    main()
