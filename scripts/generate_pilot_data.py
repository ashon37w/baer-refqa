"""Generate 300 synthetic IfQA samples for the pilot run."""
import json
from pathlib import Path
from baer_refqa.data.synthetic_generator import generate_pilot_batch
from baer_refqa.settings import Settings

def main() -> None:
    settings = Settings(repo_root=Path(__file__).resolve().parents[1])
    settings.ensure_dirs()
    rows = generate_pilot_batch(n=300, seed=2026)
    target = settings.raw_dir / "source_rows.jsonl"
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"Generated {len(rows)} rows -> {target}")

if __name__ == "__main__":
    main()
