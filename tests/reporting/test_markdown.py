from baer_refqa.reporting.markdown import render_report

def test_render_report_contains_core_metric_names() -> None:
    report = render_report(
        project_name="pilot",
        slice_rows=[
            {
                "task_slice": "pragmatic_intent",
                "n": 40,
                "asr_loss": 0.12,
                "modality_penalty": 0.04,
                "incremental_audio_value": 0.09,
                "prosody_sensitivity": 0.08,
                "label": "audio_essential",
            }
        ],
        risks=["modality penalty remains high for emotion"],
    )
    assert "# pilot Audit Report" in report
    assert "Incremental Audio Value" in report
    assert "modality penalty remains high for emotion" in report
