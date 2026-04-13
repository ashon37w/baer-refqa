"""Simulate model predictions with realistic noise for pilot evaluation."""
import random


def _noisy(base: float, noise: float, seed: int) -> float:
    rng = random.Random(seed)
    val = base + rng.gauss(0, noise)
    return max(0.0, min(1.0, val))


def simulate_condition_predictions(n_samples: int, seed: int = 42) -> list[dict]:
    """
    Simulate realistic accuracy scores across C1-C5 conditions.
    Returns list of {text_oracle, text_asr, speech_natural, speech_lexicalized, speech_revoiced}.
    """
    rows = []
    for i in range(n_samples):
        # Text oracle is strongest
        oracle = _noisy(0.78, 0.08, seed=i * 100 + seed)
        # ASR degrades oracle
        asr = _noisy(oracle - 0.12, 0.06, seed=i * 100 + 1 + seed)
        # Speech natural often matches or beats oracle (audio helps)
        speech_nat = _noisy(max(oracle, 0.75), 0.10, seed=i * 100 + 2 + seed)
        # Lexicalized speech is worse than natural (prosody stripped)
        lexical = _noisy(speech_nat - 0.18, 0.07, seed=i * 100 + 3 + seed)
        # Revoiced is similar to natural
        revoice = _noisy(speech_nat - 0.05, 0.08, seed=i * 100 + 4 + seed)
        rows.append({
            "text_oracle": round(oracle, 4),
            "text_asr": round(asr, 4),
            "speech_natural": round(speech_nat, 4),
            "speech_lexicalized": round(lexical, 4),
            "speech_revoiced": round(revoice, 4),
        })
    return rows
