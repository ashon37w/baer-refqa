"""Generate simulated C1-C5 predictions for all pilot samples."""
import json
from pathlib import Path
from baer_refqa.models.simulator import simulate_condition_predictions
from baer_refqa.settings import Settings


def main() -> None:
    settings = Settings(repo_root=Path(__file__).resolve().parents[1])
    families_path = settings.interim_dir / "semantic_families.jsonl"

    if not families_path.exists():
        print(f"Semantic families not found: {families_path} — run scripts/build_families.py first")
        return

    families = [json.loads(l) for l in families_path.open(encoding="utf-8") if l.strip()]
    predictions = simulate_condition_predictions(n_samples=len(families), seed=42)

    target = settings.artifact_dir / "audit" / "condition_predictions.jsonl"
    target.parent.mkdir(parents=True, exist_ok=True)

    with target.open("w", encoding="utf-8") as f:
        for family, pred in zip(families, predictions):
            for condition, correct in pred.items():
                f.write(json.dumps({
                    "sample_id": family["family_id"],
                    "task_slice": family["task_type"],
                    "condition": condition,
                    "correct": correct,
                }, ensure_ascii=False) + "\n")
    print(f"Generated {len(predictions)} sample predictions → {target}")


if __name__ == "__main__":
    main()
