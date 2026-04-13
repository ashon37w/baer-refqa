"""Run Whisper ASR on generated audio files."""
import json
from pathlib import Path
from tqdm import tqdm
from baer_refqa.models.asr_adapter import WhisperAdapter
from baer_refqa.settings import Settings


def main() -> None:
    settings = Settings(repo_root=Path(__file__).resolve().parents[1])
    adapter = WhisperAdapter(model_name="base")
    manifest = settings.artifact_dir / "generation" / "generation_jobs.jsonl"
    results = settings.artifact_dir / "generation" / "asr_manifest.jsonl"
    results.parent.mkdir(parents=True, exist_ok=True)

    if not manifest.exists():
        print(f"Manifest not found: {manifest} — skipping ASR")
        return

    with manifest.open("r", encoding="utf-8") as fin, results.open("w", encoding="utf-8") as fout:
        for line in tqdm(fin, desc="Running ASR"):
            job = json.loads(line)
            audio_path = Path(job["output_path"])
            if audio_path.exists():
                job["asr_text"] = adapter.transcribe(audio_path)
            else:
                job["asr_text"] = ""
            fout.write(json.dumps(job, ensure_ascii=False) + "\n")
    print(f"ASR results → {results}")


if __name__ == "__main__":
    main()
