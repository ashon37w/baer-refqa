from pathlib import Path
from baer_refqa.generation.models import GenerationJob

class CosyVoiceAdapter:
    def __init__(self, script_path: str = "third_party/cosyvoice/infer_cli.py") -> None:
        self.script_path = script_path

    def build_command(self, job: GenerationJob) -> list[str]:
        return [
            "python",
            self.script_path,
            "--text",
            job.transcript,
            "--reference-id",
            job.reference_id,
            "--mode",
            job.generation_mode,
            "--output",
            job.output_path,
        ]

    def ensure_parent_dir(self, job: GenerationJob) -> None:
        Path(job.output_path).parent.mkdir(parents=True, exist_ok=True)
