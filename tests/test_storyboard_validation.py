"""Tests for storyboard timing, scene consistency, and structure."""

import pytest
from agents.script_agent import ScriptAgent


def test_all_3_storyboards_generated_and_valid():
    agent = ScriptAgent()
    sb1 = agent._generate_storyboard_type_1()
    sb2 = agent._generate_storyboard_type_2()
    sb3 = agent._generate_storyboard_type_3()

    for sb in [sb1, sb2, sb3]:
        assert 30.0 <= sb.total_duration_seconds <= 60.0
        assert len(sb.scenes) >= 3
        assert sb.visual_hook.duration_seconds <= 4.0
        assert "crowdwisdomtrading.com" in sb.cta.lower() or len(sb.cta) > 10

        # Verify timing sequence
        current_time = 0.0
        for s in sb.scenes:
            assert s.start_time >= current_time - 0.1
            assert s.end_time > s.start_time
            current_time = s.end_time
