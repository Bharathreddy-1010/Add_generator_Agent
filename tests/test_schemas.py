"""Tests for Pydantic schema validation."""

import pytest
from schemas.ad_models import MetaAdRecord, WinningAdsDataset
from schemas.analysis_models import SingleAdAnalysis, AggregatedMarketingAnalysis, MarketingAnalysisReport
from schemas.research_models import ResearchItem, ICPResearchReport
from schemas.storyboard_models import VisualHook, Scene, Storyboard
from schemas.critic_models import ConceptScoreMetrics, ConceptEvaluation, ConceptScoresReport
from schemas.kanban_models import TaskStatus, WorkflowStage, KanbanTask, KanbanEvent


def test_meta_ad_record_validation():
    record = MetaAdRecord(
        ad_id="ad_test_01",
        advertiser="Test Broker",
        ad_text="Learn to trade without emotions. Join our pro scanner today.",
        headline="Stop Revenge Trading",
        relevance_score=9.0,
        hook_strength=8.5,
        pain_strength=9.2,
        offer_clarity=8.0
    )
    assert record.advertiser == "Test Broker"
    assert record.relevance_score == 9.0
    assert record.media_type == "video"


def test_storyboard_validation():
    hook = VisualHook(
        headline="YOU: BUY vs CROWD: SELL",
        visual_description="Split screen retail vs consensus",
        audio_cue="Record scratch",
        duration_seconds=3.0
    )
    scenes = [
        Scene(
            scene_number=1,
            start_time=0.0,
            end_time=3.0,
            duration=3.0,
            visual="Visual test",
            camera="Static",
            voiceover="Voiceover narration line",
            on_screen_text="Text 1"
        ),
        Scene(
            scene_number=2,
            start_time=3.0,
            end_time=10.0,
            duration=7.0,
            visual="Visual test 2",
            camera="Pan",
            voiceover="Voiceover line 2",
            on_screen_text="Text 2"
        ),
        Scene(
            scene_number=3,
            start_time=10.0,
            end_time=32.0,
            duration=22.0,
            visual="Visual test 3",
            camera="Zoom",
            voiceover="Voiceover line 3",
            on_screen_text="Text 3"
        )
    ]
    sb = Storyboard(
        ad_id="CWT-TEST",
        type="pain_icp",
        title="Test Storyboard",
        target_icp="Retail Trader",
        core_pain="Overload",
        marketing_angle="Consensus",
        visual_hook=hook,
        total_duration_seconds=32.0,
        scenes=scenes,
        cta="Sign up at crowdwisdomtrading.com"
    )
    assert sb.total_duration_seconds == 32.0
    assert len(sb.scenes) == 3


def test_concept_metrics_weighted_average():
    metrics = ConceptScoreMetrics(
        hook_strength=10.0,
        originality=10.0,
        visual_potential=10.0,
        pain_relevance=10.0,
        icp_relevance=10.0,
        product_relevance=10.0,
        credibility=10.0,
        clarity=10.0,
        emotional_impact=10.0,
        cta_strength=10.0
    )
    assert metrics.weighted_average() == 10.0
