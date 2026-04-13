"""Tests for model adapters — only interface tests, no inference."""
from baer_refqa.models.asr_adapter import WhisperAdapter
from baer_refqa.models.text_adapter import TextQAAdapter
from baer_refqa.models.speech_adapter import SpeechQAAdapter

def test_whisper_adapter_has_transcribe():
    adapter = WhisperAdapter(model_name="tiny")
    assert callable(adapter.transcribe)

def test_text_adapter_has_answer():
    adapter = TextQAAdapter(model_name="deepset/roberta-base-squad2")
    assert callable(adapter.answer)

def test_speech_adapter_has_score():
    adapter = SpeechQAAdapter(model_name="facebook/wav2vec2-base-960h")
    assert callable(adapter.score_transcript)
