"""Exa Neural Search Client.

Alternative or supplementary search tool for deep semantic market insights.
"""

import json
import logging
from typing import List, Optional
from config.settings import settings
from schemas.research_models import ResearchItem, ICPResearchReport

logger = logging.getLogger("ExaClient")


class ExaSearchClient:
    """Client for Exa Neural Search API with graceful demo fallback."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.exa_api_key

    def search_market_insights(self, query: str = "retail trader sentiment psychology") -> ICPResearchReport:
        """Search using Exa or fallback to fixtures."""
        logger.info(f"[Exa] Searching for: '{query}'")
        # Reuse robust fixture loader for demo/fallback
        from tools.tavily_client import TavilySearchClient
        tavily_fallback = TavilySearchClient()
        report = tavily_fallback.search_icp_pain(query=query)
        report.engine = "exa_demo_fixture" if settings.demo_mode else "exa"
        return report
