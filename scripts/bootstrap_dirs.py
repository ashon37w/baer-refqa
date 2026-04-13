from pathlib import Path
from baer_refqa.settings import Settings

def main() -> None:
    settings = Settings(repo_root=Path(__file__).resolve().parents[1])
    created = settings.ensure_dirs()
    print(f"Created/verified {len(created)} directories")

if __name__ == "__main__":
    main()
