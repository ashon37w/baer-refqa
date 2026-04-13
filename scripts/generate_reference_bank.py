"""Generate 20 synthetic Emilia reference metadata for pilot."""
import json
from pathlib import Path
from baer_refqa.data.emilia_generator import generate_emilia_batch
from baer_refqa.settings import Settings

def main() -> None:
    settings = Settings(repo_root=Path(__file__).resolve().parents[1])
    settings.ensure_dirs()
    clips = generate_emilia_batch(n=20, seed=7)
    target = settings.raw_dir / "emilia_metadata.jsonl"
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as f:
        for clip in clips:
            f.write(json.dumps(clip, ensure_ascii=False) + "\n")
    print(f"Generated {len(clips)} reference clips → {target}")

if __name__ == "__main__":
    main()
