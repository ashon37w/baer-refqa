from baer_refqa.schema import TaskType

def rewrite_task_as_qa(
    task_type: TaskType,
    utterance: str,
    label_space: list[str],
) -> str:
    labels = ", ".join(label_space)
    if task_type == "intonation":
        return f"Given the utterance '{utterance}', is it a statement, a question, or a rhetorical question? Choices: {labels}."
    if task_type == "emotion":
        return f"Given the utterance '{utterance}', which emotion best matches the delivery? Choices: {labels}."
    if task_type == "pragmatic_intent":
        return f"Which pragmatic force best matches the utterance '{utterance}'? Choices: {labels}."
    return f"Answer the counterfactual question about '{utterance}'."
