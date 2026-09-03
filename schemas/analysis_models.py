"""Pydantic schemas for marketing analysis of winning competitor and industry ads."""

from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class SingleAdAnalysis(BaseModel):
    """Deep structural marketing breakdown of a single winning ad."""
    ad_id: Optional[str] = Field(default=None)
    advertiser: str
    target_icp: str = Field(..., description="Target Ideal Customer Profile identified")
    pain_points: List[str] = Field(default_factory=list, description="Explicit and implicit user pains")
    emotional_triggers: List[str] = Field(default_factory=list, description="Fear, greed, frustration, relief, status")
    hook: str = Field(..., description="Opening visual or text hook used")
    marketing_angle: str = Field(..., description="Angle: e.g. Contrarion wisdom, AI automation, secret data")
    positioning: str = Field(..., description="How product is positioned vs alternatives")
    offer: str = Field(..., description="Front-end offer: trial, newsletter, discord access, pro plan")
    objections_handled: List[str] = Field(default_factory=list, description="Pre-empted customer doubts")
    urgency_mechanism: Optional[str] = Field(default=None, description="Scarcity or timing trigger")
    cta_pattern: str = Field(..., description="Action phrasing: e.g. 'Get the real signals before Monday'")
    creative_patterns: List[str] = Field(default_factory=list, description="Visual styles, color contrast, pacing")
    messaging_patterns: List[str] = Field(default_factory=list, description="Syntactic or psychological tropes")


class AggregatedMarketingAnalysis(BaseModel):
    """Cross-ad synthesis, pattern extraction, and ethical adaptation strategy."""
    analyzed_ads_count: int
    common_pain_points: List[str] = Field(default_factory=list)
    common_hooks: List[str] = Field(default_factory=list)
    common_marketing_angles: List[str] = Field(default_factory=list)
    repeated_concepts: List[str] = Field(default_factory=list)
    market_gaps_and_opportunities: List[str] = Field(
        default_factory=list,
        description="Weaknesses or clichés in competitor ads that CWT can exploit"
    )
    crowdwisdom_adaptation_strategy: List[str] = Field(
        default_factory=list,
        description="How CWT can adapt successful patterns ethically using real crowd consensus data"
    )
    compliance_notes: List[str] = Field(
        default_factory=list,
        description="Financial advertising guardrails (no profit guarantees, no fake win rates)"
    )


class MarketingAnalysisReport(BaseModel):
    """Complete container report saved to data/analysis/marketing_analysis.json."""
    generated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    is_mock_data: bool = Field(default=False)
    ad_analyses: List[SingleAdAnalysis] = Field(default_factory=list)
    aggregated_summary: AggregatedMarketingAnalysis
