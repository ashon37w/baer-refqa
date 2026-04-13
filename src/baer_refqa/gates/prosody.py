from dataclasses import dataclass

@dataclass(frozen=True)
class ProsodyFeatures:
    speech_rate: float
    pitch_variance: float
    terminal_slope: float
    mean_energy: float
    pause_ratio: float

def prosodic_distance(a: ProsodyFeatures, b: ProsodyFeatures) -> float:
    deltas = (
        abs(a.speech_rate - b.speech_rate) / max(abs(a.speech_rate), 1.0),
        abs(a.pitch_variance - b.pitch_variance) / max(abs(a.pitch_variance), 1.0),
        abs(a.terminal_slope - b.terminal_slope) / max(abs(a.terminal_slope), 1.0),
        abs(a.mean_energy - b.mean_energy) / max(abs(a.mean_energy), 1.0),
        abs(a.pause_ratio - b.pause_ratio) / max(abs(a.pause_ratio), 0.01),
    )
    return sum(deltas) / len(deltas)

def prosodic_contrast_pass(
    natural: ProsodyFeatures,
    contrast: ProsodyFeatures,
    min_distance: float = 0.35,
) -> bool:
    return prosodic_distance(natural, contrast) >= min_distance
