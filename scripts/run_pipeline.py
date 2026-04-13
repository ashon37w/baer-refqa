"""Single-script entry point for the full BAER/REF-QA pipeline."""
import logging
from pathlib import Path
from baer_refqa.settings import Settings
from baer_refqa.pipeline.orchestrator import BAERPipeline

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")


def main() -> None:
    settings = Settings(repo_root=Path(__file__).resolve().parents[1])
    pipeline = BAERPipeline(settings=settings, use_mock_synthesis=True)
    output = pipeline.run_full()
    print(f"\nPipeline complete → {output}")


if __name__ == "__main__":
    main()
