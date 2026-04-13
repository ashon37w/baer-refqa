from baer_refqa.text.family_builder import build_semantic_family
from baer_refqa.text.qa_rewriter import rewrite_task_as_qa

def test_build_semantic_family_normalizes_ifqa_record() -> None:
    family = build_semantic_family({
        "dataset": "IfQA",
        "record_id": "42",
        "context": " In the counterfactual world, the Eiffel Tower is in Berlin. ",
        "question": " Where is the Eiffel Tower? ",
        "answer": " Berlin ",
    })
    assert family.family_id == "ifqa::42"
    assert family.track == "track_a_semantic"
    assert family.answer == "Berlin"

def test_rewrite_task_as_qa_for_pragmatic_intent() -> None:
    rewritten = rewrite_task_as_qa(
        task_type="pragmatic_intent",
        utterance="You are coming.",
        label_space=["request", "challenge", "confirmation"],
    )
    assert "Which pragmatic force" in rewritten
    assert "request" in rewritten
