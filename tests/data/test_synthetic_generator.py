from baer_refqa.data.synthetic_generator import generate_pilot_batch

def test_generate_pilot_batch_produces_correct_count():
    rows = generate_pilot_batch(n=50, seed=42)
    assert len(rows) == 50
    for row in rows:
        assert "dataset" in row
        assert "record_id" in row
        assert "question" in row
        assert "answer" in row
        assert row["dataset"] == "ifqa"

def test_seed_produces_deterministic_output():
    rows1 = generate_pilot_batch(n=10, seed=99)
    rows2 = generate_pilot_batch(n=10, seed=99)
    assert rows1 == rows2
    assert rows1 != generate_pilot_batch(n=10, seed=100)
