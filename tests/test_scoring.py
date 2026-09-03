"""Tests for Creative Critic evaluation scoring algorithms."""

import pytest
from schemas.critic_models import ConceptScoreMetrics
from agents.creative_critic import CreativeCriticAgent
from agents.script_agent import ScriptAgent


def test_creative_critic_winner_selection(tmp_path):
    script_agent = ScriptAgent()
    storyboards = [
        script_agent._generate_storyboard_type_1(),
        script_agent._generate_storyboard_type_2(),
        script_agent._generate_storyboard_type_3(),
    ]

    critic = CreativeCriticAgent()
    winner_sb, report = critic.run(storyboards)

    assert winner_sb is not None
    assert report.winner_ad_id == winner_sb.ad_id
    assert len(report.evaluations) == 3
    # Check that highest score won
    scores = [e.composite_score for e in report.evaluations]
    assert report.evaluations[0].composite_score == max(scores)
