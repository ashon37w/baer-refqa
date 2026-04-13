from baer_refqa.audit.runner import summarize_sample_rows

def test_summarize_sample_rows_groups_conditions_by_sample() -> None:
    rows = [
        {"sample_id": "s1", "task_slice": "intonation", "condition": "text_oracle", "correct": 1.0},
        {"sample_id": "s1", "task_slice": "intonation", "condition": "text_asr", "correct": 0.0},
        {"sample_id": "s1", "task_slice": "intonation", "condition": "speech_natural", "correct": 1.1},
        {"sample_id": "s1", "task_slice": "intonation", "condition": "speech_lexicalized", "correct": 0.5},
    ]
    summaries = summarize_sample_rows(rows)
    assert len(summaries) == 1
    assert summaries[0]["audit"]["classification"] == "audio_essential"
