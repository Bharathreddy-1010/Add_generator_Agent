"""Hermes Workflow Engine.

Orchestrates the multi-agent marketing video pipeline across durable Kanban stages.
Tracks lifecycle state transitions, logs structured events, and manages agent handoffs.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from hermes.kanban_db import HermesKanbanDB
from hermes.kanban_view import HermesKanbanViewer
from schemas.kanban_models import KanbanTask, KanbanEvent, TaskStatus, WorkflowStage

logger = logging.getLogger("HermesWorkflow")


class HermesWorkflowOrchestrator:
    """Coordinates agent execution following Hermes Kanban state machine rules."""

    def __init__(self, db: HermesKanbanDB, viewer: Optional[HermesKanbanViewer] = None):
        self.db = db
        self.viewer = viewer or HermesKanbanViewer(db)
        self.current_stage = WorkflowStage.INITIALIZE
        self._initialize_pipeline_tasks()

    def _initialize_pipeline_tasks(self) -> None:
        """Set up standard pipeline tasks in kanban.db if not already present."""
        self.db.ensure_board()
        pipeline_defs = [
            (
                "task_01_ads_research",
                "Competitor & Industry Meta Ads Scraping",
                WorkflowStage.RESEARCHING_ADS,
                "AdsManager",
                [],
                "Niche: Financial Trading & Market Intelligence, Window: 30 days"
            ),
            (
                "task_02_marketing_analysis",
                "Deep Marketing & Creative Strategy Extraction",
                WorkflowStage.ANALYZING_ADS,
                "MarketingAnalyzer",
                ["task_01_ads_research"],
                "Winning ads dataset"
            ),
            (
                "task_03_icp_research",
                "Tavily/Exa Fresh ICP Pain & Market Sentiment Search",
                WorkflowStage.RESEARCHING_ICP,
                "ResearchAgent",
                ["task_02_marketing_analysis"],
                "Extracted pain angles + CWT unique product data"
            ),
            (
                "task_04_script_generation",
                "3 Distinct Video Ad Storyboard Generation",
                WorkflowStage.GENERATING_SCRIPTS,
                "ScriptAgent",
                ["task_03_icp_research"],
                "Competitor analysis + 30-day fresh research + CWT data"
            ),
            (
                "task_05_concept_critic",
                "Creative Critic Scoring & Selection",
                WorkflowStage.EVALUATING_CONCEPTS,
                "CreativeCritic",
                ["task_04_script_generation"],
                "3 Storyboards JSON"
            ),
            (
                "task_06_video_production",
                "9:16 Vertical Video Rendering & Audio Composition",
                WorkflowStage.GENERATING_VIDEO,
                "VideoAgent",
                ["task_05_concept_critic"],
                "Selected & refined winning storyboard"
            ),
        ]

        for task_id, title, stage, assignee, deps, in_summary in pipeline_defs:
            existing = self.db.get_task(task_id)
            if not existing:
                task = KanbanTask(
                    task_id=task_id,
                    title=title,
                    stage=stage,
                    assignee=assignee,
                    status=TaskStatus.TODO,
                    dependencies=deps,
                    inputs_summary=in_summary
                )
                self.db.create_task(task)

    def transition_stage(self, new_stage: WorkflowStage) -> None:
        """Advance the overall workflow stage and refresh views."""
        self.current_stage = new_stage
        logger.info(f"[Workflow Transition] Entering Stage: {new_stage.value}")

    def start_task(self, task_id: str, agent_name: str, message: str = "Task started") -> None:
        """Mark task IN_PROGRESS and log START event."""
        self.db.update_task_status(task_id, TaskStatus.IN_PROGRESS)
        event = KanbanEvent(
            task_id=task_id,
            agent=agent_name,
            event_type="START",
            message=message
        )
        self.db.log_event(event)
        logger.info(f"[{agent_name}] {message}")

    def log_decision(self, task_id: str, agent_name: str, decision: str, payload: Optional[Dict[str, Any]] = None) -> None:
        """Record an explicit agent decision."""
        self.db.update_task_status(task_id, TaskStatus.IN_PROGRESS, decision=decision)
        event = KanbanEvent(
            task_id=task_id,
            agent=agent_name,
            event_type="DECISION",
            message=decision,
            payload=payload or {}
        )
        self.db.log_event(event)
        logger.info(f"[{agent_name}] Decision: {decision}")

    def log_status(self, task_id: str, agent_name: str, status_msg: str) -> None:
        """Record an informational status update."""
        event = KanbanEvent(
            task_id=task_id,
            agent=agent_name,
            event_type="STATUS",
            message=status_msg
        )
        self.db.log_event(event)
        logger.info(f"[{agent_name}] Status: {status_msg}")

    def complete_task(
        self,
        task_id: str,
        agent_name: str,
        outputs_summary: str,
        message: str = "Task completed successfully"
    ) -> None:
        """Mark task DONE and log COMPLETE event."""
        self.db.update_task_status(task_id, TaskStatus.DONE, outputs_summary=outputs_summary)
        event = KanbanEvent(
            task_id=task_id,
            agent=agent_name,
            event_type="COMPLETE",
            message=message,
            payload={"outputs": outputs_summary}
        )
        self.db.log_event(event)
        logger.info(f"[{agent_name}] Completed: {outputs_summary}")

    def fail_task(self, task_id: str, agent_name: str, error_message: str) -> None:
        """Mark task FAILED and record error event."""
        self.db.update_task_status(task_id, TaskStatus.FAILED, outputs_summary=f"Failed: {error_message}")
        event = KanbanEvent(
            task_id=task_id,
            agent=agent_name,
            event_type="ERROR",
            message=error_message
        )
        self.db.log_event(event)
        self.transition_stage(WorkflowStage.FAILED)
        logger.error(f"[{agent_name}] FAILED: {error_message}")

    def render_board(self) -> None:
        """Display current terminal board."""
        self.viewer.print_terminal_board(self.current_stage)
