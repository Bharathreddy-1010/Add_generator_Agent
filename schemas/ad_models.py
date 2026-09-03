"""Pydantic schemas for Meta Ad models and datasets."""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class MetaAdRecord(BaseModel):
    """Normalized ad record extracted from Meta Ad Library via Apify or fixtures."""
    ad_id: Optional[str] = Field(default=None, description="Unique Ad identifier from Meta Library")
    advertiser: str = Field(..., description="Brand / advertiser name")
    headline: Optional[str] = Field(default=None, description="Ad headline or title")
    ad_text: str = Field(..., description="Primary copy / caption text of the ad")
    description: Optional[str] = Field(default=None, description="Secondary or link description")
    cta: Optional[str] = Field(default=None, description="Call to action text (e.g. Learn More, Sign Up)")
    landing_page: Optional[str] = Field(default=None, description="Destination landing page URL")
    media_type: str = Field(default="video", description="video, image, or carousel")
    first_seen_date: Optional[str] = Field(default=None, description="ISO or YYYY-MM-DD date first seen")
    last_seen_date: Optional[str] = Field(default=None, description="ISO or YYYY-MM-DD date last seen")
    source: str = Field(default="meta_ad_library", description="Data source identifier")
    url: Optional[str] = Field(default=None, description="Direct URL to ad or snapshot")

    # Evaluative / Analytical scoring (0.0 to 10.0)
    relevance_score: float = Field(default=7.0, ge=0.0, le=10.0, description="Relevance to trading niche")
    hook_strength: float = Field(default=7.0, ge=0.0, le=10.0, description="Opening pattern-interrupt strength")
    pain_strength: float = Field(default=7.0, ge=0.0, le=10.0, description="Relevance to trader pain points")
    offer_clarity: float = Field(default=7.0, ge=0.0, le=10.0, description="Clarity of the value proposition")
    marketing_angle: Optional[str] = Field(default=None, description="Core marketing angle (e.g. FOMO, herd bias, data)")
    extracted_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat(), description="Extraction timestamp")


class WinningAdsDataset(BaseModel):
    """Dataset of curated winning ads."""
    niche: str = Field(default="financial_trading_market_intelligence")
    time_window_days: int = Field(default=30)
    total_found: int
    shortlisted_count: int
    generated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    source_summary: str = Field(default="Apify Meta Ad Library Actor")
    is_mock_data: bool = Field(default=False, description="True if generated from local fixture dataset")
    ads: List[MetaAdRecord] = Field(default_factory=list)
