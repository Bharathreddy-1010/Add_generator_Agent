"""Pydantic schemas for fresh market intelligence & ICP pain research."""

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class ResearchItem(BaseModel):
    """Structured research finding from Tavily or Exa."""
    title: str = Field(..., description="Title of the article, forum thread, or post")
    url: str = Field(..., description="Direct URL of the source")
    publication_date: Optional[str] = Field(default=None, description="Publication date if available")
    source: str = Field(..., description="Origin domain (e.g. reddit.com, twitter.com, bloomberg.com)")
    extracted_insight: str = Field(..., description="Core actionable insight extracted about trader psychology/pain")
    target_icp: Optional[str] = Field(default="Retail active swing/day trader", description="Identified ICP")
    relevance_score: float = Field(default=8.5, ge=0.0, le=10.0, description="Relevance to 30-day market conditions")
    recency_window: str = Field(default="Last 30 Days")
    timestamp_retrieved: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class ICPResearchReport(BaseModel):
    """Complete research dataset saved to data/research/icp_pain_research.json."""
    query: str
    engine: str = Field(default="tavily", description="tavily, exa, or demo_fixture")
    generated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    is_mock_data: bool = Field(default=False)
    total_sources_found: int
    key_themes: List[str] = Field(default_factory=list, description="Top aggregated pain themes identified")
    items: List[ResearchItem] = Field(default_factory=list)
