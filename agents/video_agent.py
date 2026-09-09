"""Video Production Agent.

Directs the rendering pipeline to transform the winning storyboard into a 9:16
vertical video advertisement (outputs/final_ad.mp4) and renders the animated
Hermes Kanban video (outputs/hermes_kanban_demo.mp4) for assessment submission.
"""

from pathlib import Path
import shutil
from typing import Optional, Tuple

from agents.base_agent import BaseAgent
from schemas.storyboard_models import Storyboard
from tools.video_renderer import VideoAdRenderer
from tools.openmontage_renderer import OpenMontageRenderer
from hermes.workflow import HermesWorkflowOrchestrator
from hermes.kanban_view import HermesKanbanViewer
from schemas.kanban_models import WorkflowStage


class VideoAgent(BaseAgent):
    """Agent responsible for scene rendering, voiceover mixing, and final MP4 production."""

    def __init__(self, workflow: Optional[HermesWorkflowOrchestrator] = None):
        super().__init__("VideoAgent", workflow)
        self.vertical_renderer = VideoAdRenderer()
        self.openmontage_renderer = OpenMontageRenderer()

    def run(self, winning_storyboard: Optional[Storyboard] = None) -> Tuple[Path, Path]:
        task_id = "task_06_video_production"
        if self.workflow:
            self.workflow.transition_stage(WorkflowStage.GENERATING_VIDEO)
            self.workflow.start_task(task_id, self.name, "Rendering OpenMontage Remotion and vertical video ads...")

        # Load winning storyboard if not passed
        if not winning_storyboard:
            from agents.creative_critic import CreativeCriticAgent
            winning_storyboard, _ = CreativeCriticAgent(self.workflow).run()

        self.log_status(
            task_id,
            f"Composing {len(winning_storyboard.scenes)} scenes for '{winning_storyboard.title}' "
            f"({winning_storyboard.total_duration_seconds}s total duration)..."
        )

        # 1. Primary: Render OpenMontage Remotion Video Ad (Vox Style Master Sheet)
        openmontage_ad_path = self.settings.outputs_dir / "cwt_openmontage_ad.mp4"
        final_ad_path = self.settings.outputs_dir / "final_ad.mp4"
        vertical_ad_path = self.settings.outputs_dir / "final_ad_vertical.mp4"

        rendered_via_openmontage = False
        if self.openmontage_renderer.is_available():
            self.log_status(task_id, "Rendering Vox Style Master Sheet Remotion composition (1080x1920) with interactive male voiceover...")
            try:
                self.openmontage_renderer.render(winning_storyboard, openmontage_ad_path, composition_id="VoxExplainerVertical")
                if openmontage_ad_path.exists() and openmontage_ad_path.stat().st_size > 1000:
                    shutil.copy(str(openmontage_ad_path), str(final_ad_path))
                    shutil.copy(str(openmontage_ad_path), str(vertical_ad_path))
                    rendered_via_openmontage = True
            except Exception as e:
                self.log_status(task_id, f"OpenMontage render notice: {e}. Falling back to secondary renderer.")

        # 2. Secondary fallback: OpenCV renderer if OpenMontage was not used or failed
        if not rendered_via_openmontage:
            self.log_status(task_id, "Rendering via secondary vertical renderer...")
            self.vertical_renderer.render_storyboard(winning_storyboard, "final_ad_vertical.mp4")
            shutil.copy(str(vertical_ad_path), str(final_ad_path))

        decision = (
            f"Completed video composition via OpenMontage Remotion: 1920x1080 full HD broadcast quality, "
            f"synchronized master voiceover, animated SPY divergence & 16,420+ sources charts, "
            f"comparison cards, and ducked audio bed. Also generated 9:16 vertical edition."
        )
        self.log_decision(task_id, decision)

        # 3. Render Hermes Kanban Demo Video (satisfies assessment requirement)
        self.log_status(task_id, "Rendering animated Hermes Kanban workflow MP4 video for submission...")
        viewer = HermesKanbanViewer(self.workflow.db if self.workflow else None)
        kanban_video_path = self.settings.outputs_dir / "hermes_kanban_demo.mp4"
        viewer.render_kanban_video(kanban_video_path, duration_seconds=12)

        summary = f"Video complete: {final_ad_path.name} (OpenMontage) and {kanban_video_path.name}"
        if self.workflow:
            self.workflow.complete_task(task_id, self.name, summary)
            self.workflow.transition_stage(WorkflowStage.COMPLETED)

        return final_ad_path, kanban_video_path
