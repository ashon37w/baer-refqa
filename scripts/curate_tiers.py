import json
from pathlib import Path
from baer_refqa.curation.tiering import decide_tier
from baer_refqa.schema import SampleRecord, GateResult
from baer_refqa.settings import Settings


def main() -> None:
    settings = Settings(repo_root=Path(__file__).resolve().parents[1])
    # Load family data for full SampleRecord fields
    families_path = settings.interim_dir / "semantic_families.jsonl"
    families = {json.loads(l)["family_id"]: json.loads(l) for l in families_path.read_text(encoding="utf-8").splitlines() if l.strip()}
    # Load audit summaries
    audit_path = settings.artifact_dir / "audit" / "sample_audit_summary.jsonl"
    summaries = [json.loads(l) for l in audit_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    # Build enriched SampleRecords and assign tiers
    # Validity gates default to all-True for pilot (ASR pipeline not yet run on real audio)
    default_validity = GateResult(
        lexical_pass=True, prosody_pass=True, auto_label_pass=True, behavioral_pass=True
    )
    target = settings.artifact_dir / "audit" / "tiered_samples.jsonl"
    target.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with target.open("w", encoding="utf-8") as writer:
        for summary in summaries:
            fam = families.get(summary["sample_id"], {})
            sample = SampleRecord(
                sample_id=summary["sample_id"],
                family_id=summary["sample_id"],
                track=fam.get("track", "track_a_semantic"),
                task_type=fam.get("task_type", "semantic_counterfactual"),
                question=fam.get("question", ""),
                answer=fam.get("answer", ""),
                target_transcript=fam.get("target_transcript", ""),
                validity=default_validity,
                audit=summary.get("audit"),
            )
            sample.tier = decide_tier(sample)
            writer.write(json.dumps(sample.model_dump(), ensure_ascii=False) + "\n")
            count += 1
    print(f"Wrote {count} tiered samples to {target}")


if __name__ == "__main__":
    main()
