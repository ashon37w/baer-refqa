from baer_refqa.models.simulator import simulate_condition_predictions

def test_simulator_returns_all_five_conditions():
    rows = simulate_condition_predictions(n_samples=5, seed=99)
    assert len(rows) == 5
    for row in rows:
        assert "text_oracle" in row
        assert "text_asr" in row
        assert "speech_natural" in row
        assert "speech_lexicalized" in row
        assert "speech_revoiced" in row
        assert all(0.0 <= v <= 1.0 for v in row.values())

def test_simulator_is_deterministic():
    rows1 = simulate_condition_predictions(n_samples=3, seed=42)
    rows2 = simulate_condition_predictions(n_samples=3, seed=42)
    assert rows1 == rows2
    assert rows1 != simulate_condition_predictions(n_samples=3, seed=99)
