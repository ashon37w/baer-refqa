import numpy as np
from pathlib import Path
from baer_refqa.generation.cosyvoice_adapter import CosyVoiceAdapter
from baer_refqa.generation.models import GenerationJob

def test_adapter_run_job_creates_audio_file(tmp_path: Path):
    adapter = CosyVoiceAdapter(use_mock=True)
    job = GenerationJob(
        job_id="test::ref1::zero_shot",
        family_id="test",
        reference_id="ref1",
        generation_mode="zero_shot",
        transcript="Are you coming?",
        output_path=str(tmp_path / "test_audio.wav"),
    )
    output = adapter.run_job(job)
    assert output.exists()
    assert output.suffix == ".wav"

def test_adapter_build_command_includes_all_flags():
    adapter = CosyVoiceAdapter(script_path="third_party/cosyvoice/infer_cli.py")
    job = GenerationJob(
        job_id="test::ref1::zero_shot",
        family_id="test",
        reference_id="ref1",
        generation_mode="revoice",
        transcript="Hello world.",
        output_path="artifacts/generation/test.wav",
    )
    cmd = adapter.build_command(job)
    assert "--text" in cmd
    assert "Hello world." in cmd
    assert "--reference-id" in cmd
    assert "--mode" in cmd
    assert "revoice" in cmd
    assert "--output" in cmd
