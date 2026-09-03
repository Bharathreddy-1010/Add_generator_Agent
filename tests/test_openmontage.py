"""Unit tests for OpenMontage Remotion props construction and validation."""

import json
from pathlib import Path
from schemas.storyboard_models import Storyboard
from tools.openmontage_renderer import OpenMontageRenderer


def test_openmontage_props_construction():
    """Verify that OpenMontageRenderer constructs valid Remotion cuts and overlays."""
    with open("data/scripts/storyboard_2.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    storyboard = Storyboard.model_validate(data)
    renderer = OpenMontageRenderer()

    vo_path = Path("remotion-composer/public/assets/cwt_master_voiceover.wav")
    music_path = Path("remotion-composer/public/assets/ambient_bed.wav")

    props = renderer.build_remotion_props(
        storyboard=storyboard,
        voiceover_audio_path=vo_path,
        music_audio_path=music_path
    )

    assert "cuts" in props
    assert len(props["cuts"]) == 6
    assert props["theme"] == "flat-motion-graphics"

    # Verify key motion cuts
    cut_types = [c["type"] for c in props["cuts"]]
    assert "hero_title" in cut_types
    assert "stat_card" in cut_types
    assert "bar_chart" in cut_types
    assert "pie_chart" in cut_types
    assert "comparison_card" in cut_types
    assert "text_card" in cut_types

    # Verify audio wiring
    assert "audio" in props
    assert "narration" in props["audio"]
    assert props["audio"]["narration"]["src"] == "assets/cwt_master_voiceover.wav"
