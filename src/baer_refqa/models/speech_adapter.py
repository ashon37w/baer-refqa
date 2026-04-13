"""Speech model adapter for C3 (Speech-Natural) and C4 (Speech-Lexicalized)."""
from pathlib import Path
import librosa
import torch
from transformers import AutoModelForCTC, AutoProcessor


class SpeechQAAdapter:
    def __init__(self, model_name: str = "facebook/wav2vec2-base-960h"):
        self.processor = AutoProcessor.from_pretrained(model_name)
        self.model = AutoModelForCTC.from_pretrained(model_name)
        self._device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self._device)

    def score_transcript(self, audio_path: Path, transcript: str) -> float:
        """Return a pseudo-confidence score based on CTC alignment."""
        audio, sr = librosa.load(audio_path, sr=16_000)
        inputs = self.processor(audio, return_tensors="pt", sampling_rate=16_000)
        inputs = {k: v.to(self._device) for k, v in inputs.items()}
        with torch.no_grad():
            logits = self.model(**inputs).logits
        pred_ids = logits.argmax(dim=-1)
        pred_text = self.processor.batch_decode(pred_ids)[0]
        pred_clean = pred_text.lower().strip()
        ref_clean = transcript.lower().strip()
        if not ref_clean:
            return 0.0
        errors = sum(a != b for a, b in zip(pred_clean.ljust(len(ref_clean)), ref_clean.ljust(len(pred_clean))))
        return max(0.0, 1.0 - errors / max(len(pred_clean), len(ref_clean), 1))
