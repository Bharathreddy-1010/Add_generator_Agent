"""Pydantic schemas for Creative Critic evaluation, scoring, and selection."""

from datetime import datetime, timezone
from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class ConceptScoreMetrics(BaseModel):
    """1 to 10 ratings across 10 vital performance-marketing dimensions."""
    hook_strength: float = Field(..., ge=1.0, le=10.0, description="Stopping power in first 3 seconds")
    originality: float = Field(..., ge=1.0, le=10.0, description="Freshness vs generic trading ads")
    visual_potential: float = Field(..., ge=1.0, le=10.0, description="Feasibility and impact of 9:16 vertical visuals")
    pain_relevance: float = Field(..., ge=1.0, le=10.0, description="Accuracy of addressing real trader frustrations")
    icp_relevance: float = Field(..., ge=1.0, le=10.0, description="Resonance with active retail swing/day traders")
    product_relevance: float = Field(..., ge=1.0, le=10.0, description="Authentic grounding in CWT crowd intelligence")
    credibility: float = Field(..., ge=1.0, le=10.0, description="Compliance, absence of fake hype / guaranteed profit claims")
    clarity: float = Field(..., ge=1.0, le=10.0, description="Simplicity of the narrative and takeaway")
    emotional_impact: float = Field(..., ge=1.0, le=10.0, description="Tension-to-relief emotional arc")
    cta_strength: float = Field(..., ge=1.0, le=10.0, description="Frictionless, compelling call to action")

    def weighted_average(self) -> float:
        """Compute weighted overall marketing score."""
        weights = {
            "hook_strength": 0.15,
            "pain_relevance": 0.12,
            "product_relevance": 0.12,
            "credibility": 0.12,
            "visual_potential": 0.11,
            "emotional_impact": 0.10,
            "cta_strength": 0.10,
            "originality": 0.08,
            "clarity": 0.05,
            "icp_relevance": 0.05
        }
        total = (
            self.hook_strength * weights["hook_strength"] +
            self.pain_relevance * weights["pain_relevance"] +
            self.product_relevance * weights["product_relevance"] +
            self.credibility * weights["credibility"] +
            self.visual_potential * weights["visual_potential"] +
            self.emotional_impact * weights["emotional_impact"] +
            self.cta_strength * weights["cta_strength"] +
            self.originality * weights["originality"] +
            self.clarity * weights["clarity"] +
            self.icp_relevance * weights["icp_relevance"]
        )
        return round(total, 2)


class ConceptEvaluation(BaseModel):
    """Critique and score for a single storyboard concept."""
    ad_id: str
    concept_title: str
    concept_type: str
    scores: ConceptScoreMetrics
    composite_score: float
    strengths: List[str]
    weaknesses: List[str]
    refinement_recommendations: List[str]


class ConceptScoresReport(BaseModel):
    """Saved to data/analysis/concept_scores.json."""
    evaluated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    evaluations: List[ConceptEvaluation]
    winner_ad_id: str
    winner_title: str
    selection_rationale: str
    winner_improvements_applied: List[str]
