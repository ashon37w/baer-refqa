from collections import defaultdict
from baer_refqa.audit.metrics import compute_audit_scores

def summarize_sample_rows(rows: list[dict]) -> list[dict]:
    grouped: dict[str, dict] = defaultdict(dict)
    slice_lookup: dict[str, str] = {}
    for row in rows:
        grouped[row["sample_id"]][row["condition"]] = float(row["correct"])
        slice_lookup[row["sample_id"]] = row["task_slice"]

    summaries: list[dict] = []
    for sample_id, values in grouped.items():
        audit = compute_audit_scores(
            text_oracle=values["text_oracle"],
            text_asr=values["text_asr"],
            speech_natural=values["speech_natural"],
            speech_lexicalized=values["speech_lexicalized"],
        )
        summaries.append(
            {
                "sample_id": sample_id,
                "task_slice": slice_lookup[sample_id],
                "audit": audit.model_dump(),
            }
        )
    return summaries
