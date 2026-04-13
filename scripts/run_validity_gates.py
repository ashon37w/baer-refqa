import json
from pathlib import Path
from baer_refqa.gates.lexical import lexical_invariance_pass

def main() -> None:
    source = Path("artifacts/generation/asr_manifest.jsonl")
    target = Path("artifacts/gates/lexical_results.jsonl")
    target.parent.mkdir(parents=True, exist_ok=True)
    with source.open("r", encoding="utf-8") as reader, target.open("w", encoding="utf-8") as writer:
        for line in reader:
            row = json.loads(line)
            row["lexical_pass"] = lexical_invariance_pass(
                row["target_transcript"],
                row["asr_text"],
            )
            writer.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(target)

if __name__ == "__main__":
    main()
