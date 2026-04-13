"""Generate synthetic IfQA-like counterfactual QA data for pilot runs."""
import random
from typing import Any

COUNTERFACTUALS = [
    {"context": "In the counterfactual world, the Eiffel Tower is in Berlin.", "question": "Where is the Eiffel Tower?", "answer": "Berlin"},
    {"context": "In this world, the Amazon River flows north.", "question": "Which direction does the Amazon River flow?", "answer": "North"},
    {"context": "Imagine Paris is the capital of Germany.", "question": "What is the capital of Germany in this scenario?", "answer": "Paris"},
    {"context": "The sun rises in the west in this alternate reality.", "question": "Where does the sun rise?", "answer": "In the west"},
    {"context": "In this version, water boils at 50°C.", "question": "At what temperature does water boil?", "answer": "50°C"},
    {"context": "The Pacific Ocean is completely frozen.", "question": "What is the state of the Pacific Ocean?", "answer": "Frozen"},
    {"context": "Mount Everest is only 1000 meters tall in this world.", "question": "How tall is Mount Everest?", "answer": "1000 meters"},
    {"context": "The Moon orbits Earth in the opposite direction.", "question": "Which direction does the Moon orbit Earth?", "answer": "Opposite direction"},
]

def generate_pilot_batch(n: int, seed: int = 42) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    rows = []
    for i in range(n):
        cf = rng.choice(COUNTERFACTUALS)
        rows.append({
            "dataset": "ifqa",
            "record_id": str(i),
            "context": cf["context"],
            "question": cf["question"],
            "answer": cf["answer"],
        })
    return rows
