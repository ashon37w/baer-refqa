"""ASR adapter wrapping OpenAI Whisper."""
from pathlib import Path
import torch
import whisper


class WhisperAdapter:
    def __init__(self, model_name: str = "base", device: str | None = None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = whisper.load_model(model_name, device=self.device)

    def transcribe(self, audio_path: Path) -> str:
        result = self.model.transcribe(str(audio_path), fp16=self.device == "cuda")
        return result["text"].strip()
