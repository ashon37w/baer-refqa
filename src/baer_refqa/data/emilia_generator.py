"""Generate synthetic Emilia-style reference metadata for pilot runs."""
import random

UTTERANCES = [
    "Are you coming to the meeting?",
    "I think that's an excellent idea.",
    "Can you please explain that again?",
    "The results look promising.",
    "I completely disagree with that.",
    "What time should we start?",
    "This is absolutely fascinating.",
    "Could you repeat that slowly?",
    "I'm not sure about that.",
    "That sounds like a great plan.",
    "Let's discuss this tomorrow.",
    "I'm very happy to hear that.",
    "That seems quite unlikely.",
]

EMOTIONS = ["neutral", "questioning", "assertive", "uncertain", "enthusiastic"]

def generate_emilia_batch(n: int, seed: int = 7) -> list[dict]:
    rng = random.Random(seed)
    clips = []
    for i in range(n):
        clips.append({
            "reference_id": f"emilia-ref-{i:04d}",
            "language": "en",
            "speaker_id": f"spk-{i % 5}",
            "transcript": rng.choice(UTTERANCES),
            "speaking_rate": round(rng.uniform(3.5, 6.5), 2),
            "pitch_range": round(rng.uniform(80.0, 160.0), 1),
            "terminal_slope": round(rng.uniform(-25.0, -5.0), 1),
            "pause_ratio": round(rng.uniform(0.05, 0.20), 3),
            "emotion_hint": rng.choice(EMOTIONS),
        })
    return clips
