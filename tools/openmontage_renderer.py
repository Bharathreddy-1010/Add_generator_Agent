"""OpenMontage / Remotion Video Ad Production Engine.

Integrates the OpenMontage Remotion Composer to generate professional,
broadcast-quality motion-graphics video advertisements featuring:
- Hero Title hooks with dynamic typography and animated gradient meshes
- Animated Stat Cards with negative/positive market drawdown metrics
- High-contrast Bar and Pie charts for SPY divergence & 16,420+ sentiment sources
- Comparison cards contrasting lagging technicals vs. CrowdWisdom consensus
- Multi-layer audio mixing with synchronized voiceover narration and ambient music
"""

import json
import logging
import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Any, List

from config.settings import settings
from schemas.storyboard_models import Storyboard
from tools.tts_engine import VoiceoverEngine

logger = logging.getLogger("OpenMontageRenderer")


class OpenMontageRenderer:
    """Renders broadcast-quality video advertisements via OpenMontage Remotion Composer."""

    def __init__(self, composer_dir: Path | None = None):
        self.composer_dir = composer_dir or (Path(__file__).resolve().parent.parent / "remotion-composer")
        self.props_dir = self.composer_dir / "public" / "demo-props"
        self.props_dir.mkdir(parents=True, exist_ok=True)
        self.tts = VoiceoverEngine()

    def generate_full_voiceover(self, storyboard: Storyboard, output_audio: Path) -> float:
        """Synthesizes scene voiceovers and concatenates into one master audio file."""
        output_audio.parent.mkdir(parents=True, exist_ok=True)
        temp_files: List[Path] = []

        total_duration = 0.0
        for i, scene in enumerate(storyboard.scenes):
            scene_audio = self.tts.synthesize_scene_voiceover(
                scene_idx=i + 1,
                narration_text=scene.voiceover,
                target_duration=float(scene.duration)
            )
            temp_files.append(scene_audio)
            total_duration += float(scene.duration)

        # Create ffmpeg concat list
        concat_txt = output_audio.parent / "om_audio_concat.txt"
        with open(concat_txt, "w", encoding="utf-8") as f:
            for tf in temp_files:
                f.write(f"file '{tf.resolve()}'\n")

        # Concat audio files
        cmd = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", str(concat_txt),
            "-c", "copy",
            str(output_audio)
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        # Cleanup list
        if concat_txt.exists():
            concat_txt.unlink()

        logger.info(f"[OpenMontage] Master voiceover generated: {output_audio} ({total_duration:.1f}s)")
        return total_duration

    def build_remotion_props(
        self,
        storyboard: Storyboard,
        voiceover_audio_path: Path,
        music_audio_path: Path | None = None
    ) -> Dict[str, Any]:
        """Constructs Remotion JSON props following OpenMontage schema."""
        # Calculate scene timestamps
        cuts: List[Dict[str, Any]] = []
        current_time = 0.0

        # Scene 1: Hero Hook
        s1 = storyboard.scenes[0]
        d1 = float(s1.duration)
        cuts.append({
            "id": "cwt-hook",
            "source": "",
            "type": "hero_title",
            "in_seconds": round(current_time, 2),
            "out_seconds": round(current_time + d1, 2),
            "text": "84% OF RETAIL TRADERS ARE WRONG.",
            "heroSubtitle": "When social sentiment screams 'buy', smart money prepares the exit.",
            "backgroundColor": "#0A0F1D"
        })
        current_time += d1

        # Scene 2: The Agitation / Stat Card
        s2 = storyboard.scenes[1] if len(storyboard.scenes) > 1 else s1
        d2 = float(s2.duration)
        cuts.append({
            "id": "cwt-pain-stat",
            "source": "",
            "type": "stat_card",
            "in_seconds": round(current_time, 2),
            "out_seconds": round(current_time + d2, 2),
            "stat": "-$4,250",
            "subtitle": "Average retail drawdown from moving stop losses into euphoric hype.",
            "accentColor": "#EF4444",
            "backgroundColor": "#0A0F1D"
        })
        current_time += d2

        # Scene 3: The Proof / SPY Divergence Bar Chart
        s3 = storyboard.scenes[2] if len(storyboard.scenes) > 2 else s2
        d3 = float(s3.duration)
        cuts.append({
            "id": "cwt-spy-divergence",
            "source": "",
            "type": "bar_chart",
            "in_seconds": round(current_time, 2),
            "out_seconds": round(current_time + d3, 2),
            "title": "SPY Sentiment Divergence Signal (Case Study)",
            "chartData": [
                {"label": "Retail Bull Hype", "value": 84},
                {"label": "Market Drop (Trap)", "value": 32},
                {"label": "CWT Reversal Capture", "value": 76}
            ],
            "chartColors": ["#EF4444", "#F59E0B", "#10B981"],
            "showGrid": True,
            "showValues": True,
            "backgroundColor": "#0A0F1D"
        })
        current_time += d3

        # Scene 4: Engine Breakdown / Pie Donut
        s4 = storyboard.scenes[3] if len(storyboard.scenes) > 3 else s3
        d4 = float(s4.duration)
        cuts.append({
            "id": "cwt-data-breakdown",
            "source": "",
            "type": "pie_chart",
            "in_seconds": round(current_time, 2),
            "out_seconds": round(current_time + d4, 2),
            "title": "Aggregating 16,420+ Real-Time Market Sources",
            "donut": True,
            "centerLabel": "16,420+",
            "centerValue": "Sources",
            "chartData": [
                {"label": "FinTwit Sentiment", "value": 45},
                {"label": "Reddit Subreddits", "value": 35},
                {"label": "Financial Wire Feeds", "value": 20}
            ],
            "chartColors": ["#3B82F6", "#8B5CF6", "#10B981"],
            "showLegend": True,
            "backgroundColor": "#0A0F1D"
        })
        current_time += d4

        # Scene 5: Comparison Card
        s5 = storyboard.scenes[4] if len(storyboard.scenes) > 4 else s4
        d5 = float(s5.duration)
        cuts.append({
            "id": "cwt-comparison",
            "source": "",
            "type": "comparison_card",
            "in_seconds": round(current_time, 2),
            "out_seconds": round(current_time + d5, 2),
            "title": "Traditional Lagging Indicators vs CrowdWisdom",
            "leftLabel": "12 Lagging Indicators",
            "leftValue": "Conflicting signals\nVisual screen fatigue\nConstant FOMO trap",
            "rightLabel": "CrowdWisdom Consensus",
            "rightValue": "Decisive crowd sentiment\n76% reversal predictive accuracy\nZero chart indicator clutter",
            "backgroundColor": "#0A0F1D",
            "accentColor": "#10B981"
        })
        current_time += d5

        # Scene 6: Finale CTA
        s6 = storyboard.scenes[5] if len(storyboard.scenes) > 5 else s5
        d6 = float(s6.duration)
        cuts.append({
            "id": "cwt-cta-card",
            "source": "",
            "type": "text_card",
            "in_seconds": round(current_time, 2),
            "out_seconds": round(current_time + d6, 2),
            "text": "Stop Guessing. Trade The Consensus.",
            "subtitle": "crowdwisdomtrading.com — Free Screening Tools Included.",
            "color": "#10B981",
            "backgroundColor": "#0A0F1D"
        })
        current_time += d6

        # Overlays
        overlays = [
            {
                "type": "stat_reveal",
                "in_seconds": 1.2,
                "out_seconds": 3.8,
                "text": "84% Hype Trap",
                "subtitle": "Institutional Liquidity Exit",
                "accentColor": "#EF4444",
                "position": "bottom-right"
            },
            {
                "type": "section_title",
                "in_seconds": round(d1 + 0.5, 2),
                "out_seconds": round(d1 + 3.0, 2),
                "text": "The Retail Trap",
                "subtitle": "Why indicators fail during high volatility",
                "accentColor": "#F59E0B"
            }
        ]

        # Audio configuration
        audio_config: Dict[str, Any] = {
            "narration": {
                "src": "assets/cwt_master_voiceover.wav",
                "volume": 1.0
            }
        }
        if music_audio_path and music_audio_path.exists():
            audio_config["music"] = {
                "src": "assets/ambient_bed.wav",
                "volume": 0.18,
                "fadeInSeconds": 1.0,
                "fadeOutSeconds": 1.5,
                "loop": True
            }

        props: Dict[str, Any] = {
            "theme": "flat-motion-graphics",
            "cuts": cuts,
            "overlays": overlays,
            "captions": [],
            "audio": audio_config
        }
        return props

    def render(
        self,
        storyboard: Storyboard,
        output_video: Path,
        composition_id: str = "Explainer"
    ) -> Path:
        """Executes full OpenMontage Remotion render pipeline."""
        output_video.parent.mkdir(parents=True, exist_ok=True)

        # 1. Synthesize master voiceover inside public assets
        audio_dir = self.composer_dir / "public" / "assets"
        audio_dir.mkdir(parents=True, exist_ok=True)
        master_vo = audio_dir / "cwt_master_voiceover.wav"
        self.generate_full_voiceover(storyboard, master_vo)

        # 2. Ambient bed audio in public assets
        ambient_audio = audio_dir / "ambient_bed.wav"
        existing_ambient = Path("outputs/assets/ambient_bed.wav")
        if existing_ambient.exists():
            shutil.copy(str(existing_ambient), str(ambient_audio))
        elif not ambient_audio.exists():
            from tools.video_renderer import VideoAdRenderer
            dummy_renderer = VideoAdRenderer()
            dummy_renderer._generate_ambient_audio_bed(ambient_audio, duration=60.0)

        # 3. Build Remotion Props
        props = self.build_remotion_props(
            storyboard=storyboard,
            voiceover_audio_path=master_vo,
            music_audio_path=ambient_audio
        )

        props_file = self.props_dir / "cwt-openmontage-ad.json"
        with open(props_file, "w", encoding="utf-8") as f:
            json.dump(props, f, indent=2)

        logger.info(f"[OpenMontage] Prepared props: {props_file}")

        # 4. Invoke Remotion CLI
        npx_cmd = shutil.which("npx") or "npx"
        temp_render_path = output_video.parent / "renders" / f"temp_{output_video.name}"
        temp_render_path.parent.mkdir(parents=True, exist_ok=True)

        cmd = [
            npx_cmd,
            "remotion",
            "render",
            "src/index.tsx",
            composition_id,
            str(temp_render_path.resolve()),
            "--props",
            str(props_file.resolve()),
            "--codec",
            "h264"
        ]

        logger.info(f"[OpenMontage] Executing Remotion render in {self.composer_dir}...")
        res = subprocess.run(
            cmd,
            cwd=str(self.composer_dir),
            capture_output=True,
            text=True
        )

        if res.returncode != 0:
            logger.error(f"[OpenMontage] Remotion render failed: {res.stderr}")
            raise RuntimeError(f"Remotion render failed with exit code {res.returncode}: {res.stderr}")

        # Move to final path
        shutil.move(str(temp_render_path), str(output_video))
        logger.info(f"[OpenMontage] Render completed successfully: {output_video} ({output_video.stat().st_size / 1024 / 1024:.1f} MB)")
        return output_video
