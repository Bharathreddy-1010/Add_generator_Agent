"""Video Production Agent.

Directs the rendering pipeline to transform the winning storyboard into a 9:16
vertical video advertisement (outputs/final_ad.mp4) and renders the animated
Hermes Kanban video (outputs/hermes_kanban_demo.mp4) for assessment submission.
"""

from pathlib import Path
from typing import Optional, Tuple

from agents.base_agent import BaseAgent
from schemas.storyboard_models import Storyboard
from tools.video_renderer import VideoAdRenderer
from hermes.workflow import HermesWorkflowOrchestrator
from hermes.kanban_view import HermesKanbanViewer
from schemas.kanban_models import WorkflowStage


class VideoAgent(BaseAgent):
    """Agent responsible for scene rendering, voiceover mixing, and final MP4 production."""

    def __init__(self, workflow: Optional[HermesWorkflowOrchestrator] = None):
        super().__init__("VideoAgent", workflow)
        self.renderer = VideoAdRenderer()

    def run(self, winning_storyboard: Optional[Storyboard] = None) -> Tuple[Path, Path]:
        task_id = "task_06_video_production"
        if self.workflow:
            self.workflow.transition_stage(WorkflowStage.GENERATING_VIDEO)
            self.workflow.start_task(task_id, self.name, "Rendering 9:16 vertical video ad and Kanban video...")

        # Load winning storyboard if not passed
        if not winning_storyboard:
            from agents.creative_critic import CreativeCriticAgent
            winning_storyboard, _ = CreativeCriticAgent(self.workflow).run()

        self.log_status(
            task_id,
            f"Composing {len(winning_storyboard.scenes)} scenes for '{winning_storyboard.title}' "
            f"({winning_storyboard.total_duration_seconds}s total duration)..."
        )

        # Render Final Ad MP4
        final_ad_path = self.renderer.render_storyboard(winning_storyboard, "final_ad.mp4")

        decision = (
            f"Completed video composition: 1080x1920 vertical format, synchronized voiceover narration, "
            f"dynamic Vox-style charts, and ambient audio bed ducking."
        )
        self.log_decision(task_id, decision)

        # Render Hermes Kanban Demo Video (satisfies assessment requirement)
        self.log_status(task_id, "Rendering animated Hermes Kanban workflow MP4 video for submission...")
        viewer = HermesKanbanViewer(self.workflow.db if self.workflow else None)
        kanban_video_path = self.settings.outputs_dir / "hermes_kanban_demo.mp4"
        viewer.render_kanban_video(kanban_video_path, duration_seconds=12)

        summary = f"Video complete: {final_ad_path.name} ({winning_storyboard.total_duration_seconds}s) and {kanban_video_path.name}"
        if self.workflow:
            self.workflow.complete_task(task_id, self.name, summary)
            self.workflow.transition_stage(WorkflowStage.COMPLETED)

        return final_ad_path, kanban_video_path
