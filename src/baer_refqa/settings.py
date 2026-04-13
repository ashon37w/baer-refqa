from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Settings:
    repo_root: Path

    @property
    def raw_dir(self) -> Path:
        return self.repo_root / "data" / "raw"

    @property
    def interim_dir(self) -> Path:
        return self.repo_root / "data" / "interim"

    @property
    def processed_dir(self) -> Path:
        return self.repo_root / "data" / "processed"

    @property
    def artifact_dir(self) -> Path:
        return self.repo_root / "artifacts"

    @property
    def report_dir(self) -> Path:
        return self.repo_root / "reports"

    def ensure_dirs(self) -> tuple[Path, ...]:
        paths = (
            self.raw_dir,
            self.interim_dir,
            self.processed_dir,
            self.artifact_dir / "reference_bank",
            self.artifact_dir / "generation",
            self.artifact_dir / "gates",
            self.artifact_dir / "audit",
            self.report_dir,
        )
        for path in paths:
            path.mkdir(parents=True, exist_ok=True)
        return paths
