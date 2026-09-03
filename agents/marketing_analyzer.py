"""Marketing Analysis Agent.

Extracts deep psychological, positioning, and creative patterns from successful ads
without copying competitors, delivering structured findings for CrowdWisdom adaptation.
"""

import json
from pathlib import Path
from typing import Optional

from agents.base_agent import BaseAgent
from tools.llm_client import StructuredLLMClient
from schemas.ad_models import WinningAdsDataset
from schemas.analysis_models import MarketingAnalysisReport, SingleAdAnalysis, AggregatedMarketingAnalysis
from hermes.workflow import HermesWorkflowOrchestrator
from schemas.kanban_models import WorkflowStage


class MarketingAnalyzerAgent(BaseAgent):
    """Agent responsible for structural marketing and psychological analysis."""

    def __init__(self, workflow: Optional[HermesWorkflowOrchestrator] = None):
        super().__init__("MarketingAnalyzer", workflow)
        self.llm = StructuredLLMClient()

    def run(self, ads_dataset: Optional[WinningAdsDataset] = None) -> MarketingAnalysisReport:
        task_id = "task_02_marketing_analysis"
        if self.workflow:
            self.workflow.transition_stage(WorkflowStage.ANALYZING_ADS)
            self.workflow.start_task(task_id, self.name, "Deconstructing competitor hooks, emotional triggers, and offers...")

        # Load ads if not passed directly
        if not ads_dataset:
            ads_file = self.settings.ads_dir / "winning_ads.json"
            if ads_file.exists():
                with open(ads_file, "r", encoding="utf-8") as f:
                    ads_dataset = WinningAdsDataset.model_validate_json(f.read())
            else:
                from agents.ads_manager import AdsManagerAgent
                ads_dataset = AdsManagerAgent(self.workflow).run()

        self.log_status(task_id, f"Analyzing {len(ads_dataset.ads)} selected competitor ad records...")

        # Define fallback factory for demo / offline mode
        def fallback_analysis() -> MarketingAnalysisReport:
            fixture_file = self.settings.fixtures_dir / "sample_analysis.json"
            with open(fixture_file, "r", encoding="utf-8") as f:
                return MarketingAnalysisReport.model_validate_json(f.read())

        system_prompt = (
            "You are an elite direct-response marketing strategist specializing in financial technology and trading tools. "
            "Analyze the provided competitor ads. Deconstruct their ICP, core pain points, emotional triggers, hook formulas, "
            "positioning, offers, and objections. Synthesize cross-cutting patterns and identify ethical opportunities for CrowdWisdomTrading."
        )

        user_prompt = f"Here is the dataset of winning Meta ads to analyze:\n{ads_dataset.model_dump_json()}"

        report = self.llm.generate_structured(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_model=MarketingAnalysisReport,
            fallback_factory=fallback_analysis
        )
        report.is_mock_data = self.settings.demo_mode or not self.llm.client

        decision = (
            f"Identified primary market gap: Competitors push complex chart indicators; "
            f"CrowdWisdom will position as 'Decisive Crowd Consensus' with zero indicator clutter."
        )
        self.log_decision(task_id, decision)

        # Save output
        out_file = self.settings.analysis_dir / "marketing_analysis.json"
        out_file.parent.mkdir(parents=True, exist_ok=True)
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(report.model_dump_json(indent=2))

        summary = f"Analysis completed: {len(report.ad_analyses)} ads deconstructed; strategic gap identified."
        if self.workflow:
            self.workflow.complete_task(task_id, self.name, summary)

        return report
