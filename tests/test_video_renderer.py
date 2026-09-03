"""Tests for Audio and Video rendering utilities."""

import pytest
from pathlib import Path
from tools.tts_engine import VoiceoverEngine
from tools.video_renderer import VideoAdRenderer
from agents.script_agent import ScriptAgent


def test_voiceover_synthesis(tmp_path):
    engine = VoiceoverEngine(tmp_path)
    wav_path = engine.synthesize_scene_voiceover(
        scene_idx=1,
        narration_text="This is a test of the speech engine.",
        target_duration=3.0
    )
    assert wav_path.exists()
    assert wav_path.stat().st_size > 0


def test_ambient_audio_generation(tmp_path):
    renderer = VideoAdRenderer()
    out_wav = tmp_path / "ambient.wav"
    renderer._generate_ambient_audio_bed(out_wav, duration=2.0)
    assert out_wav.exists()
    assert out_wav.stat().st_size > 0
