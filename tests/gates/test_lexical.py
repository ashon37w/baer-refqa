from baer_refqa.gates.lexical import lexical_invariance_pass

def test_lexical_invariance_blocks_prompt_leak_and_high_cer() -> None:
    assert lexical_invariance_pass("You are coming.", "You are coming.", max_cer=0.10)
    assert not lexical_invariance_pass("You are coming.", "assistant: You are coming.", max_cer=0.10)
    assert not lexical_invariance_pass("You are coming.", "You are leaving.", max_cer=0.10)
