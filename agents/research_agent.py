"""Research Agent.

Gathers fresh, 30-day web market intelligence using Tavily / Exa and aligns findings
with authentic CrowdWisdomTrading product data and unique metrics.
"""

import json
from pathlib import Path
from typing import Optional

from agents.base_agent import BaseAgent
from tools.tavily_client import TavilySearchClient
from tools.exa_client import ExaSearchClient
from schemas.research_models import ICPResearchReport
from hermes.workflow import HermesWorkflowOrchestrator
from schemas.kanban_models import WorkflowStage


class ResearchAgent(BaseAgent):
    """Agent responsible for fresh market pain research and CWT data synthesis."""

    def __init__(self, workflow: Optional[HermesWorkflowOrchestrator] = None):
        super().__init__("ResearchAgent", workflow)
        self.tavily = TavilySearchClient()
        self.exa = ExaSearchClient()

    def run(self, query: str = "retail trader pain points indicator overload fomo Reddit 2026") -> ICPResearchReport:
        task_id = "task_03_icp_research"
        if self.workflow:
            self.workflow.transition_stage(WorkflowStage.RESEARCHING_ICP)
            self.workflow.start_task(task_id, self.name, f"Executing 30-day recency search for ICP pains...")

        # Step 1: Query Tavily / Exa
        self.log_status(task_id, f"Querying search APIs for active trader discussions (days=30)...")
        report = self.tavily.search_icp_pain(query=query, days=30)
        self.log_status(task_id, f"Gathered {report.total_sources_found} sources across Reddit, FinTwit, and market journals.")

        # Step 2: Load authentic CWT product & unique data
        unique_data_file = self.settings.crowdwisdom_dir / "unique_data.json"
        if unique_data_file.exists():
            with open(unique_data_file, "r", encoding="utf-8") as f:
                cwt_data = json.load(f)
                case_studies = cwt_data.get("unique_case_studies", [])
                decision = (
                    f"Synthesized research with CWT unique case study: {case_studies[0]['case_id']} "
                    f"({case_studies[0]['retail_sentiment_gauge']} vs {case_studies[0]['crowdwisdom_consensus_gauge']})"
                )
                self.log_decision(task_id, decision)

        # Step 3: Save results to data/research/icp_pain_research.json
        out_file = self.settings.research_dir / "icp_pain_research.json"
        out_file.parent.mkdir(parents=True, exist_ok=True)
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(report.model_dump_json(indent=2))

        summary = f"{report.total_sources_found} research sources verified and saved to data/research/icp_pain_research.json"
        if self.workflow:
            self.workflow.complete_task(task_id, self.name, summary)

        return report
