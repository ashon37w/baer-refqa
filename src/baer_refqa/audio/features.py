from dataclasses import dataclass
from pathlib import Path
import librosa
import numpy as np

@dataclass(frozen=True)
class ProsodyVector:
    speech_rate: float
    pitch_variance: float
    terminal_slope: float
    mean_energy: float
    pause_ratio: float

def extract_prosody_features(audio_path: Path) -> ProsodyVector:
    audio, sr = librosa.load(audio_path, sr=None)
    duration = max(len(audio) / sr, 1e-6)
    rms = librosa.feature.rms(y=audio)[0]
    f0 = librosa.yin(audio, fmin=75, fmax=400, sr=sr)
    voiced = f0[np.isfinite(f0)]
    terminal = voiced[-10:] if len(voiced) >= 10 else voiced
    terminal_slope = float(terminal[-1] - terminal[0]) if len(terminal) >= 2 else 0.0
    speech_segments = librosa.effects.split(audio, top_db=30)
    speech_rate = float(len(speech_segments) / duration)
    pause_ratio = float((np.abs(audio) < 0.01).mean())
    return ProsodyVector(
        speech_rate=speech_rate,
        pitch_variance=float(np.var(voiced)) if len(voiced) else 0.0,
        terminal_slope=terminal_slope,
        mean_energy=float(np.mean(rms)),
        pause_ratio=pause_ratio,
    )
