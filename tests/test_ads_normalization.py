"""Tests for Ad normalization, deduplication, and recency filtering."""

import pytest
from datetime import datetime, timedelta
from tools.apify_client import ApifyMetaAdsClient


def test_ad_normalization_and_deduplication():
    client = ApifyMetaAdsClient()
    raw_items = [
        {
            "id": "1",
            "pageName": "TradingView",
            "adCopy": "Stop staring at 12 charts at once. Consolidate your edge today with automated alerts.",
            "firstSeen": "2026-08-20",
            "lastSeen": "2026-08-28"
        },
        # Duplicate copy
        {
            "id": "2",
            "pageName": "TradingView Duplicate",
            "adCopy": "Stop staring at 12 charts at once. Consolidate your edge today with automated alerts.",
            "firstSeen": "2026-08-21",
            "lastSeen": "2026-08-29"
        },
        # Old ad beyond 30 days
        {
            "id": "3",
            "pageName": "Old Advertiser",
            "adCopy": "Ancient ad from last year that should definitely be filtered out by date logic.",
            "firstSeen": "2025-01-01",
            "lastSeen": "2025-01-20"
        }
    ]

    normalized = client._normalize_raw_items(raw_items, days_back=30)
    # Should deduplicate id 2 and filter out id 3
    assert len(normalized) == 1
    assert normalized[0].advertiser == "TradingView"
