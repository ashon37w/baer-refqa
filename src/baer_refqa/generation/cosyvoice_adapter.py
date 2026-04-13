"""CosyVoice command builder and execution adapter."""
from pathlib import Path
import subprocess
import shutil
import numpy as np
import soundfile as sf
from baer_refqa.generation.models import GenerationJob


class CosyVoiceAdapter:
    def __init__(
        self,
        script_path: str = "third_party/cosyvoice/infer_cli.py",
        use_mock: bool = False,
    ) -> None:
        self.script_path = script_path
        self.use_mock = use_mock

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

    def run_job(self, job: GenerationJob) -> Path:
        """Execute a generation job. Returns path to output audio file."""
        output_path = Path(job.output_path)
        self.ensure_parent_dir(job)

        if self.use_mock:
            return self._mock_synthesis(job, output_path)

        cmd = self.build_command(job)
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"CosyVoice failed: {result.stderr}")
        return output_path

    def _mock_synthesis(self, job: GenerationJob, output_path: Path) -> Path:
        """Generate a synthetic sine-wave audio when CosyVoice is unavailable."""
        sr = 22050
        duration = min(len(job.transcript) * 0.08, 5.0)
        t = np.linspace(0, duration, int(sr * duration))
        # Mix of harmonics for a more natural-ish tone
        freq = 220.0
        audio = (
            0.3 * np.sin(2 * np.pi * freq * t) +
            0.15 * np.sin(2 * np.pi * freq * 2 * t) +
            0.1 * np.sin(2 * np.pi * freq * 3 * t)
        ).astype(np.float32)
        sf.write(output_path, audio, sr)
        return output_path
