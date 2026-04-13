from pathlib import Path

def main() -> None:
    source = Path("data/raw/emilia_metadata.jsonl")
    target = Path("artifacts/reference_bank/reference_bank.jsonl")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
    print(target)

if __name__ == "__main__":
    main()
