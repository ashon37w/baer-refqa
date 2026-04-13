from pathlib import Path
from baer_refqa.settings import Settings

def test_settings_expose_repo_relative_stage_dirs(tmp_path: Path) -> None:
    settings = Settings(repo_root=tmp_path)
    assert settings.raw_dir == tmp_path / "data" / "raw"
    assert settings.processed_dir == tmp_path / "data" / "processed"
    assert settings.report_dir == tmp_path / "reports"
    settings.ensure_dirs()
    assert settings.processed_dir.exists()
    assert settings.report_dir.exists()
