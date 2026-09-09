"""OpenMontage / Remotion Video Ad Production Engine (Vox Style Master Sheet).

Integrates the OpenMontage Remotion Composer to generate authentic,
documentary-collage video advertisements following the Vox Style Master Sheet:
- Archival Tan background (#C9BB9C) with subtle halftone texture and 2% camera drift
- Ink Black (#1A1A1A) condensed bold typography with animated Hot Red (#B62E1F) underline swipe
- Cutout figures and charts with white sticker border and 6px offset Hot Red drop shadow
- Mustard (#D9A441) annotation labels ("Fig. X - [Label]")
- Synchronized lower-third newsroom subtitles for every spoken line
- Per-sequence audio locking ensuring 100% audio-video synchronization
"""

import json
import logging
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Tuple

from config.settings import settings
from schemas.storyboard_models import Storyboard, Scene
from tools.tts_engine import VoiceoverEngine

logger = logging.getLogger("OpenMontageRenderer")


class OpenMontageRenderer:
    """Renders broadcast-quality video advertisements via OpenMontage Remotion Composer."""

    def __init__(self, composer_dir: Path | None = None):
        self.composer_dir = composer_dir or (Path(__file__).resolve().parent.parent / "remotion-composer")
        self.props_dir = self.composer_dir / "public" / "demo-props"
        self.props_dir.mkdir(parents=True, exist_ok=True)
        self.tts = VoiceoverEngine()

    def generate_synchronized_voiceovers(
        self,
        storyboard: Storyboard
    ) -> List[Dict[str, Any]]:
        """Synthesizes scene voiceovers individually and stores in Remotion public assets."""
        audio_dir = self.composer_dir / "public" / "assets"
        audio_dir.mkdir(parents=True, exist_ok=True)
        scene_info: List[Dict[str, Any]] = []

        for i, scene in enumerate(storyboard.scenes):
            scene_num = i + 1
            # Synthesize natural human speech and measure exact duration
            out_wav, measured_dur = self.tts.synthesize_and_measure(
                scene_idx=scene_num,
                narration_text=scene.voiceover,
                target_duration=float(scene.duration)
            )
            # Copy to remotion public assets for direct Sequence audio playback
            target_asset = audio_dir / f"vox_scene_{scene_num:02d}.wav"
            shutil.copy(str(out_wav), str(target_asset))

            scene_info.append({
                "scene_number": scene_num,
                "duration": measured_dur,
                "audioSrc": f"assets/vox_scene_{scene_num:02d}.wav",
                "voiceover": scene.voiceover,
                "on_screen_text": scene.on_screen_text,
                "visual": scene.visual,
            })

        logger.info(f"[OpenMontage] Synthesized {len(scene_info)} synchronized scene audio tracks in {audio_dir}")
        return scene_info

    def _build_vox_cut_for_scene(
        self,
        scene_data: Dict[str, Any],
        in_sec: float,
        out_sec: float
    ) -> Dict[str, Any]:
        """Dynamically build cut data matching the scene's semantic content."""
        scene_idx = scene_data["scene_number"]
        vo = scene_data["voiceover"]
        text_lower = f"{vo} {scene_data.get('visual', '')} {scene_data.get('on_screen_text', '')}".lower()

        # Defaults
        visual_type = "hook_stat"
        headline = "THE RETAIL TRAP"
        subtitle = "When social sentiment screams 'buy', smart money prepares the exit."
        figure_label = f"Retail Sentiment Analysis #{scene_idx}"
        stat_number = 84
        stat_prefix = ""
        stat_suffix = "%"
        stat_label = "Retail Conviction Buying Peak Noise"
        is_negative = False
        alert_text = "⚠️ WARNING: INSTITUTIONAL SMART MONEY EXITING INTO RETAIL FOMO"

        if "divergence" in text_lower or "spy" in text_lower or "market fell" in text_lower or "reversal" in text_lower:
            visual_type = "chart_divergence"
            headline = "76% INSTITUTIONAL DIVERGENCE"
            subtitle = "Spotting institutional divergence 48 hours before the 3.8% market drop."
            figure_label = "SPY Divergence Case Report"
            stat_number = 76
            stat_suffix = "%"
            stat_label = "SPY Reversal Predictive Capture Accuracy"
            alert_text = "● CWT CONSENSUS EXIT: 48 HOURS BEFORE MARKET DROP"
        elif "16,000" in text_lower or "16,420" in text_lower or "sources" in text_lower or "radar" in text_lower or "youtube" in text_lower:
            visual_type = "sources_radar"
            headline = "16,420+ SOURCES MONITORED"
            subtitle = "Filtering out bot spam across YouTube, Reddit, and FinTwit to track real conviction."
            figure_label = "Collective Sentiment Radar"
            stat_number = 16420
            stat_suffix = "+"
            stat_label = "Verified Market Predictions Distilled Daily"
            alert_text = "89.4% SOCIAL NOISE FILTERED • REAL CONVICTION IDENTIFIED"
        elif "gilad" in text_lower or "veteran" in text_lower or "track record" in text_lower or "execution-ready" in text_lower or "risk" in text_lower:
            visual_type = "founder_track_record"
            headline = "VERIFIED TRACK RECORD"
            subtitle = "Transparent, execution-ready signals with pre-defined risk."
            figure_label = "Institutional Credentials & Methodology"
            stat_number = 25
            stat_suffix = "+ Yrs"
            stat_label = "Market Experience • Founder Gilad Bar-Ilan"
            alert_text = "FOUNDED BY GILAD BAR-ILAN • 25+ YEARS VERIFIED TRADING EXPERIENCE"
        elif "exit liquidity" in text_lower or "vacuum" in text_lower or "comparison" in text_lower or "reaction" in text_lower:
            visual_type = "comparison_cards"
            headline = "STOP BEING EXIT LIQUIDITY"
            subtitle = "Use collective data to trade the reaction, not the emotional hype."
            figure_label = "Trade The Reaction, Not The Hype"
            stat_number = 3
            stat_suffix = "x R/R"
            stat_label = "Disciplined Risk to Reward Profile"
            alert_text = "DISCIPLINED EXECUTION: TRADE THE REACTION, NOT THE HYPE"
        elif "free predictions" in text_lower or "20 free" in text_lower or "crowdwisdomtrading.com" in text_lower or "visit" in text_lower or "outlook" in text_lower:
            visual_type = "cta_offer"
            headline = "GET 20 FREE PREDICTIONS"
            subtitle = "Test CrowdWisdom collective market intelligence today."
            figure_label = "Free Platform Access Pass"
            stat_number = 20
            stat_suffix = " Free"
            stat_label = "Prediction Credits Included with Zero Obligation"
            alert_text = "ZERO CREDIT CARD REQUIRED • VISIT CROWDWISDOMTRADING.COM"
        elif "indicator" in text_lower or "14" in text_lower or "paralysis" in text_lower:
            visual_type = "hook_stat"
            headline = "14 INDICATORS CANNOT SAVE YOU"
            subtitle = "Conflicting technicals cause analysis paralysis and late entries."
            figure_label = "Indicator Overload & Hesitation"
            stat_number = 4250
            stat_prefix = "$"
            stat_label = "Average Retail Drawdown from Revenge Trading"
            is_negative = True
            alert_text = "ANALYSIS PARALYSIS: 14 INDICATORS CANNOT PREVENT DRAWDOWN"
        else:
            # Fallback hook
            visual_type = "hook_stat"
            headline = "THE RETAIL TRAP"
            subtitle = "When social sentiment screams 'buy', smart money prepares the exit."
            figure_label = f"Retail Sentiment #{scene_idx}"
            stat_number = 84
            stat_suffix = "%"
            stat_label = "Retail Conviction Buying Peak Noise"

        return {
            "id": f"vox-cut-{scene_idx}",
            "scene_number": scene_idx,
            "in_seconds": in_sec,
            "out_seconds": out_sec,
            "visualType": visual_type,
            "headline": headline,
            "subtitle": subtitle,
            "figureLabel": figure_label,
            "figureNumber": scene_idx,
            "statNumber": stat_number,
            "statPrefix": stat_prefix,
            "statSuffix": stat_suffix,
            "statLabel": stat_label,
            "isNegative": is_negative,
            "voiceoverText": vo,
            "alertText": alert_text,
            "audioSrc": scene_data["audioSrc"],
            "durationSeconds": round(out_sec - in_sec, 2),
        }

    def build_vox_remotion_props(
        self,
        storyboard: Storyboard,
        scene_info: List[Dict[str, Any]],
        music_audio_path: Path | None = None
    ) -> Dict[str, Any]:
        """Constructs Remotion JSON props with per-sequence audio and content alignment."""
        cuts: List[Dict[str, Any]] = []
        current_time = 0.0

        for scene_data in scene_info:
            dur = scene_data["duration"]
            in_sec = round(current_time, 2)
            out_sec = round(current_time + dur, 2)

            cut_dict = self._build_vox_cut_for_scene(scene_data, in_sec, out_sec)
            cuts.append(cut_dict)
            current_time += dur

        audio_config: Dict[str, Any] = {}
        if music_audio_path and music_audio_path.exists():
            audio_config["music"] = {
                "src": "assets/ambient_bed.wav",
                "volume": 0.12,
            }

        return {
            "cuts": cuts,
            "audio": audio_config,
        }

    def build_remotion_props(
        self,
        storyboard: Storyboard,
        voiceover_audio_path: Path,
        music_audio_path: Path | None = None
    ) -> Dict[str, Any]:
        """Backward-compatible props builder for standard Remotion Explainer."""
        cuts: List[Dict[str, Any]] = []
        current_time = 0.0

        cut_types = ["hero_title", "stat_card", "bar_chart", "pie_chart", "comparison_card", "text_card"]
        for idx, scene in enumerate(storyboard.scenes[:6]):
            d = float(scene.duration)
            c_type = cut_types[idx % len(cut_types)]
            cut_data: Dict[str, Any] = {
                "id": f"cwt-cut-{idx+1}",
                "source": "",
                "type": c_type,
                "in_seconds": round(current_time, 2),
                "out_seconds": round(current_time + d, 2),
                "backgroundColor": "#C9BB9C",
                "accentColor": "#B62E1F",
            }
            if c_type == "hero_title":
                cut_data["text"] = "84% OF RETAIL TRADERS ARE WRONG."
                cut_data["heroSubtitle"] = "When social hype screams buy, smart money prepares the exit."
            elif c_type == "stat_card":
                cut_data["stat"] = "-$4,250"
                cut_data["subtitle"] = "Average retail drawdown from chasing lagging indicators."
            elif c_type == "bar_chart":
                cut_data["title"] = "SPY Sentiment Divergence Signal"
                cut_data["chartData"] = [
                    {"label": "Retail Hype", "value": 84},
                    {"label": "Market Trap", "value": 32},
                    {"label": "CWT Exit", "value": 76}
                ]
            elif c_type == "pie_chart":
                cut_data["title"] = "Aggregating 16,420+ Market Sources"
                cut_data["donut"] = True
                cut_data["chartData"] = [
                    {"label": "FinTwit", "value": 45},
                    {"label": "Reddit", "value": 35},
                    {"label": "Wires", "value": 20}
                ]
            elif c_type == "comparison_card":
                cut_data["title"] = "Indicators vs Consensus"
                cut_data["leftLabel"] = "14 Indicators"
                cut_data["leftValue"] = "Conflicting Signals"
                cut_data["rightLabel"] = "CrowdWisdom"
                cut_data["rightValue"] = "Decisive Alpha"
            else:
                cut_data["text"] = "Stop Guessing. Trade The Consensus."
                cut_data["subtitle"] = "crowdwisdomtrading.com"

            cuts.append(cut_data)
            current_time += d

        return {
            "theme": "flat-motion-graphics",
            "cuts": cuts,
            "overlays": [],
            "captions": [],
            "audio": {
                "narration": {"src": "assets/cwt_master_voiceover.wav", "volume": 1.0}
            }
        }

    def render(
        self,
        storyboard: Storyboard,
        output_video: Path,
        composition_id: str = "VoxExplainerVertical"
    ) -> Path:
        """Executes full OpenMontage Remotion render pipeline with Vox Style Master Sheet."""
        output_video.parent.mkdir(parents=True, exist_ok=True)

        # 1. Synthesize individual synchronized scene voiceovers inside public assets
        scene_info = self.generate_synchronized_voiceovers(storyboard)

        # 2. Ambient bed audio in public assets
        audio_dir = self.composer_dir / "public" / "assets"
        ambient_audio = audio_dir / "ambient_bed.wav"
        existing_ambient = Path("outputs/assets/ambient_bed.wav")
        if existing_ambient.exists():
            shutil.copy(str(existing_ambient), str(ambient_audio))
        elif not ambient_audio.exists():
            from tools.video_renderer import VideoAdRenderer
            dummy_renderer = VideoAdRenderer()
            dummy_renderer._generate_ambient_audio_bed(ambient_audio, duration=60.0)

        # 3. Build Vox Remotion Props with frame-accurate scene timestamps & per-sequence audio
        props = self.build_vox_remotion_props(
            storyboard=storyboard,
            scene_info=scene_info,
            music_audio_path=ambient_audio
        )

        props_file = self.props_dir / "cwt-vox-ad.json"
        with open(props_file, "w", encoding="utf-8") as f:
            json.dump(props, f, indent=2)

        logger.info(f"[OpenMontage] Prepared synchronized Vox props: {props_file}")

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

        logger.info(f"[OpenMontage] Executing Remotion render ({composition_id}) in {self.composer_dir}...")
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
