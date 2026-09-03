"""Ads Manager Agent.

Searches, collects, filters, and ranks competitor and industry Meta ads from the last 30 days.
"""

import json
from pathlib import Path
from typing import Optional

from agents.base_agent import BaseAgent
from tools.apify_client import ApifyMetaAdsClient
from schemas.ad_models import WinningAdsDataset
from hermes.workflow import HermesWorkflowOrchestrator
from schemas.kanban_models import WorkflowStage


class AdsManagerAgent(BaseAgent):
    """Agent responsible for sourcing and ranking winning competitor ads."""

    def __init__(self, workflow: Optional[HermesWorkflowOrchestrator] = None):
        super().__init__("AdsManager", workflow)
        self.apify_client = ApifyMetaAdsClient()

    def run(self, days_back: int = 30) -> WinningAdsDataset:
        task_id = "task_01_ads_research"
        if self.workflow:
            self.workflow.transition_stage(WorkflowStage.RESEARCHING_ADS)
            self.workflow.start_task(task_id, self.name, f"Initiating Meta Ads research for last {days_back} days...")

        # Step 1: Collect ads
        self.log_status(task_id, "Connecting to Meta Ad Library via Apify Actor...")
        dataset = self.apify_client.fetch_recent_ads(
            search_terms=["trading indicators", "market sentiment", "stock signals", "crypto trading intelligence"],
            days_back=days_back,
            max_items=25
        )

        self.log_status(task_id, f"Discovered {dataset.total_found} ads; {dataset.shortlisted_count} meet 30-day relevance criteria.")

        # Step 2: Decision on ranking & shortlisting
        top_ad = dataset.ads[0] if dataset.ads else None
        top_hook = top_ad.headline if top_ad else "None"
        decision = f"Shortlisted top {len(dataset.ads)} ads. Strongest competitor hook: '{top_hook}'"
        self.log_decision(task_id, decision)

        # Step 3: Save results to data/ads/winning_ads.json
        out_file = self.settings.ads_dir / "winning_ads.json"
        out_file.parent.mkdir(parents=True, exist_ok=True)
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(dataset.model_dump_json(indent=2))

        summary = f"{len(dataset.ads)} ads saved to data/ads/winning_ads.json"
        if self.workflow:
            self.workflow.complete_task(task_id, self.name, summary)

        return dataset
