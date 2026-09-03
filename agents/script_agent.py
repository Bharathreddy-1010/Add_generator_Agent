"""Script Agent.

Generates 3 radically distinct, 30-45 second video advertisement storyboards:
1. Type 1: Current Pain + ICP (The Solo Trader Trap / Indicator Overload)
2. Type 2: CrowdWisdom Unique Data (The 78% Reversal Signal & 16,420+ Sources)
3. Type 3: CWT Trading Decision Value (Execution-Ready Plans / Overcoming Emotion)
"""

import json
from pathlib import Path
from typing import List, Optional

from agents.base_agent import BaseAgent
from tools.llm_client import StructuredLLMClient
from schemas.storyboard_models import Storyboard, Scene, VisualHook
from schemas.analysis_models import MarketingAnalysisReport
from schemas.research_models import ICPResearchReport
from hermes.workflow import HermesWorkflowOrchestrator
from schemas.kanban_models import WorkflowStage


class ScriptAgent(BaseAgent):
    """Agent responsible for writing scene-by-scene video storyboards."""

    def __init__(self, workflow: Optional[HermesWorkflowOrchestrator] = None):
        super().__init__("ScriptAgent", workflow)
        self.llm = StructuredLLMClient()

    def run(
        self,
        analysis_report: Optional[MarketingAnalysisReport] = None,
        research_report: Optional[ICPResearchReport] = None
    ) -> List[Storyboard]:
        task_id = "task_04_script_generation"
        if self.workflow:
            self.workflow.transition_stage(WorkflowStage.GENERATING_SCRIPTS)
            self.workflow.start_task(task_id, self.name, "Creating 3 distinctly different video ad storyboards...")

        # Generate Storyboard 1: Pain + ICP
        self.log_status(task_id, "Generating Concept 1: Pain + ICP ('The Solo Trader Trap')...")
        sb1 = self._generate_storyboard_type_1()
        self._save_storyboard(sb1, "storyboard_1.json")

        # Generate Storyboard 2: Unique Data
        self.log_status(task_id, "Generating Concept 2: Unique Data ('The 78% Reversal Signal')...")
        sb2 = self._generate_storyboard_type_2()
        self._save_storyboard(sb2, "storyboard_2.json")

        # Generate Storyboard 3: CWT Decision & Results Value
        self.log_status(task_id, "Generating Concept 3: Decision & Execution Edge ('Execution Over Emotion')...")
        sb3 = self._generate_storyboard_type_3()
        self._save_storyboard(sb3, "storyboard_3.json")

        decision = (
            f"Crafted 3 distinct creative angles: "
            f"1. Pain/Overload ({sb1.total_duration_seconds}s), "
            f"2. Unique Data/Divergence ({sb2.total_duration_seconds}s), "
            f"3. Execution/Cockpit ({sb3.total_duration_seconds}s). Ready for Creative Critic scoring."
        )
        self.log_decision(task_id, decision)

        summary = "3 storyboards generated and validated in data/scripts/."
        if self.workflow:
            self.workflow.complete_task(task_id, self.name, summary)

        return [sb1, sb2, sb3]

    def _generate_storyboard_type_1(self) -> Storyboard:
        """Concept 1: Pain + ICP — The Solo Trader Trap."""
        scenes = [
            Scene(
                scene_number=1,
                start_time=0.0,
                end_time=3.0,
                duration=3.0,
                visual="Split-screen glitch: A retail trader eagerly hits BUY CALLS on SPY, while red warning tape flashes across the screen.",
                camera="Fast punch-in zoom into trading button",
                voiceover="You just hit buy on a green breakout candle. But what if 80% of the crowd is already dumping?",
                on_screen_text="YOU: BUYING CALLS ⚠️\nCROWD: DUMPING EXIT LIQUIDITY",
                sound_effect="sub_drop_record_scratch",
                music="high_tension_electronic",
                transition="cut"
            ),
            Scene(
                scene_number=2,
                start_time=3.0,
                end_time=9.0,
                duration=6.0,
                visual="Screen filled with 14 chaotic overlapping indicators (MACD, RSI, Bollinger Bands). Text overlay strikes them out with red X.",
                camera="Rapid pan across cluttered monitor",
                voiceover="Staring at 14 indicators doesn't give you clarity. It gives you analysis paralysis, late entries, and revenge trading.",
                on_screen_text="14 INDICATORS CANNOT PREVENT REVENGE TRADES",
                sound_effect="glitch_whoosh",
                music="driving_bassline",
                transition="fade"
            ),
            Scene(
                scene_number=3,
                start_time=9.0,
                end_time=17.0,
                duration=8.0,
                visual="Chaotic screen collapses cleanly into CrowdWisdom's streamlined consensus radar. Glowing blue beam pinpoints true sentiment.",
                camera="Smooth zoom out to sleek dark-mode dashboard",
                voiceover="CrowdWisdom tracks over 16,000 verified trader predictions, stripping out social noise to reveal real market consensus before the move.",
                on_screen_text="16,420+ SOURCES DISTILLED • 89.4% NOISE FILTERED",
                sound_effect="data_sweep_hum",
                music="modern_tech_pulse",
                transition="slide_left"
            ),
            Scene(
                scene_number=4,
                start_time=17.0,
                end_time=25.0,
                duration=8.0,
                visual="Clear execution plan appears on screen: SPY entry level, upside target, and defined invalidation stop.",
                camera="Static focused macro shot",
                voiceover="No guesswork. Just high-conviction trade ideas with pre-calculated entries, targets, and invalidation stops.",
                on_screen_text="ENTRY: $482.50 • TARGET: $488.20 • DEFINED STOP: $479.80",
                sound_effect="interface_beep_confirm",
                music="focused_momentum",
                transition="fade"
            ),
            Scene(
                scene_number=5,
                start_time=25.0,
                end_time=32.0,
                duration=7.0,
                visual="Split comparison: Stressed trader staring at messy screen vs disciplined trader calmly following CWT weekly outlook.",
                camera="Side-by-side contrast slider",
                voiceover="Stop trading in a vacuum. Trade with the verified collective intelligence of thousands of market veterans.",
                on_screen_text="STOP GUESSING. TRADE WITH CONSENSUS.",
                sound_effect="uplifting_swell",
                music="inspiring_crescendo",
                transition="fade"
            ),
            Scene(
                scene_number=6,
                start_time=32.0,
                end_time=38.0,
                duration=6.0,
                visual="High-contrast gold & cyan CTA card with pulsing button and domain crowdwisdomtrading.com.",
                camera="Center locked logo lockup",
                voiceover="Get this week's top 5 crowd consensus trades free. Click below to start.",
                on_screen_text="GET FREE WEEKLY OUTLOOK\ncrowdwisdomtrading.com",
                sound_effect="chime_payoff",
                music="warm_outro_pad",
                transition="fade"
            ),
        ]
        return Storyboard(
            ad_id="CWT-STORYBOARD-01-PAIN-ICP",
            type="pain_icp",
            title="The Solo Trader Trap",
            target_icp="Active retail swing and day traders overwhelmed by conflicting indicators",
            core_pain="Analysis paralysis, late entries into social hype, and emotional revenge trading",
            marketing_angle="Indicator Clutter vs Decisive Collective Intelligence",
            visual_hook=VisualHook(
                headline="YOU: BUYING CALLS vs CROWD: DUMPING",
                visual_description="Split-screen retail trade execution vs institutional crowd exit divergence.",
                audio_cue="Record scratch into sudden electronic bass drop",
                duration_seconds=3.0
            ),
            total_duration_seconds=38.0,
            scenes=scenes,
            cta="Get the top 5 crowd consensus trades free at crowdwisdomtrading.com",
            sources=["Reddit r/Daytrading survey 2026", "CWT unique trader psychology data"]
        )

    def _generate_storyboard_type_2(self) -> Storyboard:
        """Concept 2: Unique Data — The 78% Reversal Signal."""
        scenes = [
            Scene(
                scene_number=1,
                start_time=0.0,
                end_time=3.0,
                duration=3.0,
                visual="High-contrast Vox-style counter rapidly rolling up: 'RETAIL FOMO: 84% LONG' suddenly flashes RED.",
                camera="Fast tilt-down with dynamic motion blur",
                voiceover="When 84% of retail traders are screaming 'buy' on social media, you're usually looking at a trap.",
                on_screen_text="RETAIL HYPE: 84% LONG ⚠️\nINSTITUTIONAL TRAP INCOMING",
                sound_effect="alarm_heartbeat_drop",
                music="fast_pulse_synth",
                transition="cut"
            ),
            Scene(
                scene_number=2,
                start_time=3.0,
                end_time=10.0,
                duration=7.0,
                visual="SPY chart showing retail chasing top candles, while CrowdWisdom's proprietary consensus index dives 48 hours earlier.",
                camera="Animated camera tracking the divergence line",
                voiceover="During the last market cycle, our AI detected a 76% institutional divergence 48 hours before the market fell 3.8%.",
                on_screen_text="CASE STUDY: 76% DIVERGENCE DETECTED 48H BEFORE REVERSAL",
                sound_effect="data_ticker_chirp",
                music="analytical_electronic",
                transition="slide_left"
            ),
            Scene(
                scene_number=3,
                start_time=10.0,
                end_time=18.0,
                duration=8.0,
                visual="Dynamic network visualization showing 16,420 independent trader inputs collapsing into 3 actionable levels.",
                camera="3D node convergence effect",
                voiceover="We monitor over 16,000 active trader sources across YouTube, Reddit, and FinTwit, filtering out bot spam and tracking where real conviction lies.",
                on_screen_text="16,420 TRADERS MONITORED • SMART CONVICTION TRACKED",
                sound_effect="network_lock_sound",
                music="deep_groove",
                transition="fade"
            ),
            Scene(
                scene_number=4,
                start_time=18.0,
                end_time=26.0,
                duration=8.0,
                visual="Execution card with verified transparent track record badge and founder Gilad Bar-Ilan's 25-year credentials.",
                camera="Slow push in on risk metrics",
                voiceover="Founded by 25-year market veteran Gilad Bar-Ilan, CrowdWisdom gives you transparent, execution-ready signals with pre-defined risk.",
                on_screen_text="TRANSPARENT TRACK RECORD • 25+ YEARS MARKET EXPERIENCE",
                sound_effect="subtle_confirm_ping",
                music="confidence_swell",
                transition="fade"
            ),
            Scene(
                scene_number=5,
                start_time=26.0,
                end_time=33.0,
                duration=7.0,
                visual="Before/After bar chart showing capital preserved vs retail drawdown.",
                camera="Horizontal sweep",
                voiceover="Don't be someone else's exit liquidity. Use data to trade the reaction, not the hype.",
                on_screen_text="STOP BEING EXIT LIQUIDITY • TRADE WITH VERIFIED DATA",
                sound_effect="whoosh_punch",
                music="epic_drive",
                transition="fade"
            ),
            Scene(
                scene_number=6,
                start_time=33.0,
                end_time=39.0,
                duration=6.0,
                visual="Cyan & gold CTA card with free access badge and URL.",
                camera="Static impact lockup",
                voiceover="Test CrowdWisdom with 20 free predictions. Visit crowdwisdomtrading.com today.",
                on_screen_text="GET 20 FREE PREDICTIONS\ncrowdwisdomtrading.com",
                sound_effect="clean_bell_ding",
                music="fade_out_pad",
                transition="fade"
            ),
        ]
        return Storyboard(
            ad_id="CWT-STORYBOARD-02-UNIQUE-DATA",
            type="unique_data",
            title="The 78% Reversal Signal",
            target_icp="Skeptical data-driven traders looking for authentic institutional edge",
            core_pain="Getting trapped at market tops as retail exit liquidity",
            marketing_angle="Empirical Divergence & 16,420-Trader Collective Intelligence",
            visual_hook=VisualHook(
                headline="RETAIL HYPE: 84% LONG vs 76% DIVERGENCE",
                visual_description="Fast ticking FOMO counter slamming into bright red divergence alert.",
                audio_cue="Alarm pulse into deep electronic sub bass drop",
                duration_seconds=3.0
            ),
            total_duration_seconds=39.0,
            scenes=scenes,
            cta="Unlock 20 free prediction credits at crowdwisdomtrading.com",
            sources=["CrowdWisdom SPY Reversal Case Study", "Gilad Bar-Ilan market briefings"]
        )

    def _generate_storyboard_type_3(self) -> Storyboard:
        """Concept 3: CWT Trading Decision Value — Execution Over Emotion."""
        scenes = [
            Scene(
                scene_number=1,
                start_time=0.0,
                end_time=3.0,
                duration=3.0,
                visual="A trader's finger hesitating over the buy button as price violently whipsaws up and down.",
                camera="Intense macro close-up on sweating finger",
                voiceover="Hesitating on your entries? Moving your stop-loss mid-trade? That's not a market problem. That's a conviction problem.",
                on_screen_text="HESITATING ON ENTRIES?\nMOVING YOUR STOPS?",
                sound_effect="tension_string_riser",
                music="dark_ambient_tension",
                transition="cut"
            ),
            Scene(
                scene_number=2,
                start_time=3.0,
                end_time=10.0,
                duration=7.0,
                visual="Split screen showing emotional revenge trade cycle (-$850 loss) vs disciplined trade execution (+Risk Controlled).",
                camera="Fast whip pan to the right",
                voiceover="Over 70% of traders blow accounts because emotions take the wheel the second a trade moves against them.",
                on_screen_text="EMOTIONAL TRADING = ACCOUNT BLOWUPS",
                sound_effect="dull_thud",
                music="steady_rhythmic_beat",
                transition="fade"
            ),
            Scene(
                scene_number=3,
                start_time=10.0,
                end_time=18.0,
                duration=8.0,
                visual="CrowdWisdom Decision Cockpit loads: Clean 3-tier card displaying Entry, Target 1, Target 2, and Risk Invalidation level.",
                camera="Smooth gliding tracking shot",
                voiceover="CrowdWisdom replaces doubt with structured execution. Every setup comes with pre-calculated entry points, profit targets, and hard risk invalidation levels.",
                on_screen_text="DEFINED ENTRY • TARGET 1 & 2 • HARD INVALIDATION STOP",
                sound_effect="sci_fi_interface_hum",
                music="positive_electronic_arpeggio",
                transition="slide_left"
            ),
            Scene(
                scene_number=4,
                start_time=18.0,
                end_time=25.0,
                duration=7.0,
                visual="Live consensus dial moving from 50% neutral to 82% bullish conviction with glowing green confirmation checks.",
                camera="Dynamic tilt on glowing dial",
                voiceover="Powered by the collective intelligence of thousands of experienced traders, so you execute with cold, calculated discipline.",
                on_screen_text="EXECUTE WITH COLD DISCIPLINE",
                sound_effect="confirmation_chime",
                music="driving_forward_motion",
                transition="fade"
            ),
            Scene(
                scene_number=5,
                start_time=25.0,
                end_time=32.0,
                duration=7.0,
                visual="Trader calmly reviewing weekly execution plan with cup of coffee in hand as alert sounds.",
                camera="Clean cinematic medium shot",
                voiceover="Spend less time stressing over charts and more time executing high-probability setups.",
                on_screen_text="LESS STRESS. MORE STRUCTURE.",
                sound_effect="gentle_whoosh",
                music="triumphant_build",
                transition="fade"
            ),
            Scene(
                scene_number=6,
                start_time=32.0,
                end_time=37.0,
                duration=5.0,
                visual="High-impact finale card with weekly outlook invitation and website URL.",
                camera="Centered hero logo layout",
                voiceover="Join the community. Read our free weekly outlook at crowdwisdomtrading.com.",
                on_screen_text="JOIN THE CROWD EDGE\ncrowdwisdomtrading.com",
                sound_effect="crisp_snare_hit",
                music="resolving_chords",
                transition="fade"
            ),
        ]
        return Storyboard(
            ad_id="CWT-STORYBOARD-03-CWT-VALUE",
            type="cwt_results",
            title="Execution Over Emotion",
            target_icp="Experienced traders struggling with emotional discipline and moving stop-losses",
            core_pain="Hesitation, revenge trading, lack of conviction in trade setups",
            marketing_angle="Disciplined Structured Execution vs Emotional Second-Guessing",
            visual_hook=VisualHook(
                headline="HESITATING ON ENTRIES? MOVING YOUR STOPS?",
                visual_description="Extreme close-up on trader finger freezing over buy button amidst volatility.",
                audio_cue="Tension string riser into sudden silence",
                duration_seconds=3.0
            ),
            total_duration_seconds=37.0,
            scenes=scenes,
            cta="Join free weekly market outlook at crowdwisdomtrading.com",
            sources=["Retail trading behavioral psychology studies", "CWT Execution Plans"]
        )

    def _save_storyboard(self, storyboard: Storyboard, filename: str) -> None:
        out_path = self.settings.scripts_dir / filename
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(storyboard.model_dump_json(indent=2))
