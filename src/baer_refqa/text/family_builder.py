import re
from baer_refqa.schema import SemanticFamily

def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()

def build_semantic_family(raw: dict[str, str]) -> SemanticFamily:
    source_dataset = raw["dataset"].lower()
    source_id = raw["record_id"]
    context = normalize_text(raw.get("context", ""))
    question = normalize_text(raw["question"])
    answer = normalize_text(raw["answer"])
    transcript = normalize_text(raw.get("utterance", question))
    return SemanticFamily(
        family_id=f"{source_dataset}::{source_id}",
        source_dataset=source_dataset,
        source_id=source_id,
        track="track_a_semantic",
        task_type="semantic_counterfactual",
        context=context,
        prompt_utterance=transcript,
        question=question,
        answer=answer,
        target_transcript=transcript,
    )
