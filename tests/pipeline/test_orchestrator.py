from baer_refqa.pipeline.orchestrator import BAERPipeline

def test_pipeline_has_required_stages():
    stages = BAERPipeline.list_stages()
    assert "synthesis" in stages
    assert "asr" in stages
    assert "audit" in stages
    assert "tiering" in stages

def test_pipeline_accepts_use_mock_flag(tmp_path):
    from baer_refqa.settings import Settings
    settings = Settings(repo_root=tmp_path)
    pipeline = BAERPipeline(settings=settings, use_mock_synthesis=True)
    assert pipeline.use_mock_synthesis is True
