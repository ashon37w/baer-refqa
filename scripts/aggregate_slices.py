"""Aggregate audit summaries into per-slice metrics for the report."""
import json
from collections import defaultdict
from pathlib import Path
from baer_refqa.settings import Settings


def main() -> None:
    settings = Settings(repo_root=Path(__file__).resolve().parents[1])

    summaries_path = settings.artifact_dir / "audit" / "sample_audit_summary.jsonl"
    summaries = [json.loads(l) for l in summaries_path.read_text(encoding="utf-8").splitlines() if l.strip()]

    by_slice: dict[str, dict] = defaultdict(lambda: defaultdict(list))
    for row in summaries:
        sl = row["task_slice"]
        audit = row["audit"]
        by_slice[sl]["asr_loss"].append(audit["asr_loss"])
        by_slice[sl]["modality_penalty"].append(audit["modality_penalty"])
        by_slice[sl]["incremental_audio_value"].append(audit["incremental_audio_value"])
        by_slice[sl]["prosody_sensitivity"].append(audit["prosody_sensitivity"])
        by_slice[sl]["labels"].append(audit["classification"])

    slice_rows = []
    for sl, vals in sorted(by_slice.items()):
        n = len(vals["asr_loss"])
        slice_rows.append({
            "task_slice": sl,
            "n": n,
            "asr_loss": sum(vals["asr_loss"]) / n,
            "modality_penalty": sum(vals["modality_penalty"]) / n,
            "incremental_audio_value": sum(vals["incremental_audio_value"]) / n,
            "prosody_sensitivity": sum(vals["prosody_sensitivity"]) / n,
            "label": max(set(vals["labels"]), key=vals["labels"].count),
        })

    risks = []
    for row in slice_rows:
        if row["modality_penalty"] > 0.1:
            risks.append(f"[{row['task_slice']}] Modality penalty {row['modality_penalty']:.3f} exceeds 0.1 — review audio necessity.")
        if row["prosody_sensitivity"] < 0.1:
            risks.append(f"[{row['task_slice']}] Prosody sensitivity {row['prosody_sensitivity']:.3f} below 0.1 — model may be insensitive to prosodic variation.")

    payload = {
        "project_name": "BAER/REF-QA Pilot",
        "slice_rows": slice_rows,
        "risks": risks,
    }

    target = settings.artifact_dir / "audit" / "slice_summary.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote slice summary ({len(slice_rows)} slices) to {target}")


if __name__ == "__main__":
    main()
