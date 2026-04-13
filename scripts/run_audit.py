import json
from pathlib import Path
from baer_refqa.audit.runner import summarize_sample_rows

def main() -> None:
    source = Path("artifacts/audit/condition_predictions.jsonl")
    rows = [
        json.loads(line)
        for line in source.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    summaries = summarize_sample_rows(rows)
    target = Path("artifacts/audit/sample_audit_summary.jsonl")
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as handle:
        for row in summaries:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(target)

if __name__ == "__main__":
    main()
