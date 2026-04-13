from baer_refqa.gates.prosody import ProsodyFeatures, prosodic_contrast_pass

def test_prosodic_contrast_requires_meaningful_feature_distance() -> None:
    natural = ProsodyFeatures(
        speech_rate=4.8,
        pitch_variance=120.0,
        terminal_slope=-18.0,
        mean_energy=0.14,
        pause_ratio=0.09,
    )
    flattened = ProsodyFeatures(
        speech_rate=4.8,
        pitch_variance=22.0,
        terminal_slope=-2.0,
        mean_energy=0.10,
        pause_ratio=0.03,
    )
    assert prosodic_contrast_pass(natural, flattened, min_distance=0.35)
