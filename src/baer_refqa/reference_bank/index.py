from baer_refqa.reference_bank.models import ReferenceClip, ReferenceQuery

def score_reference(query: ReferenceQuery, clip: ReferenceClip) -> float:
    if clip.language != query.language:
        return float("-inf")
    score = 0.0
    score -= abs(clip.speaking_rate - query.speaking_rate)
    score -= 0.01 * abs(clip.pitch_range - query.pitch_range)
    score -= 0.05 * abs(clip.terminal_slope - query.terminal_slope)
    if query.emotion_hint and clip.emotion_hint == query.emotion_hint:
        score += 0.5
    return score

def rank_references(
    query: ReferenceQuery,
    clips: list[ReferenceClip],
    top_k: int = 5,
) -> list[ReferenceClip]:
    ranked = sorted(clips, key=lambda clip: score_reference(query, clip), reverse=True)
    return ranked[:top_k]
