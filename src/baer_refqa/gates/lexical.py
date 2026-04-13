from rapidfuzz.distance import Levenshtein

def normalized_cer(reference: str, hypothesis: str) -> float:
    return Levenshtein.normalized_distance(reference, hypothesis)

def lexical_invariance_pass(reference: str, hypothesis: str, max_cer: float = 0.08) -> bool:
    lowered = hypothesis.lower()
    if "assistant:" in lowered or "system:" in lowered:
        return False
    return normalized_cer(reference, hypothesis) <= max_cer
