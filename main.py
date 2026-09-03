#!/usr/bin/env python3
"""Main Entrypoint and CLI for CrowdWisdomTrading Hermes Video Ads Agent System.

Usage:
    python main.py                   # Run complete pipeline in configured mode
    python main.py --demo            # Force DEMO_MODE with verified fixtures
    python main.py --full-run        # Run all 6 agents end-to-end
    python main.py --ads-only        # Run only Ads Manager Agent
    python main.py --scripts-only    # Run up to 3 storyboards generation
    python main.py --video-only      # Render final video from winner storyboard
    python main.py --kanban-board    # Show current Hermes Kanban task board
    python main.py --kanban-video    # Render animated Hermes Kanban MP4 video
"""

import sys
import argparse
import logging
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

from config.settings import settings
from hermes.kanban_db import HermesKanbanDB
from hermes.workflow import HermesWorkflowOrchestrator
from hermes.kanban_view import HermesKanbanViewer
from agents.ads_manager import AdsManagerAgent
from agents.marketing_analyzer import MarketingAnalyzerAgent
from agents.research_agent import ResearchAgent
from agents.script_agent import ScriptAgent
from agents.creative_critic import CreativeCriticAgent
from agents.video_agent import VideoAgent

console = Console()


def setup_logging(debug: bool = False) -> None:
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S"
    )


def print_banner() -> None:
    banner_text = (
        "[bold cyan]CROWDWISDOM TRADING[/bold cyan]  •  [bold yellow]HERMES AI MARKETING VIDEO ADS AGENT[/bold yellow]\n"
        "[dim]Multi-Agent Kanban Orchestration  •  Apify  •  Tavily/Exa  •  Vox-Style 9:16 Video Engine[/dim]"
    )
    console.print(Panel(banner_text, box=box.DOUBLE, border_style="cyan"))


def print_final_summary(final_ad_path: Path, kanban_video_path: Path) -> None:
    """Print complete summary table of all outputs."""
    table = Table(
        title="✨ PIPELINE EXECUTION COMPLETED SUCCESSFULLY ✨",
        box=box.ROUNDED,
        header_style="bold magenta",
        expand=True
    )
    table.add_column("Deliverable / Stage", style="bold cyan", width=30)
    table.add_column("Output File Path", style="white")
    table.add_column("Status", style="bold green", width=15)

    table.add_row("1. Winning Meta Ads (30d)", "data/ads/winning_ads.json", "✅ Saved")
    table.add_row("2. Marketing Analysis Report", "data/analysis/marketing_analysis.json", "✅ Saved")
    table.add_row("3. ICP Pain Research (30d)", "data/research/icp_pain_research.json", "✅ Saved")
    table.add_row("4. Storyboard 1 (Pain+ICP)", "data/scripts/storyboard_1.json", "✅ Saved")
    table.add_row("5. Storyboard 2 (Unique Data)", "data/scripts/storyboard_2.json", "✅ Saved")
    table.add_row("6. Storyboard 3 (CWT Value)", "data/scripts/storyboard_3.json", "✅ Saved")
    table.add_row("7. Creative Critic Evaluation", "data/analysis/concept_scores.json", "✅ Saved")
    table.add_row("8. FINAL ADVERTISEMENT VIDEO", str(final_ad_path), "🎬 1080x1920 MP4")
    table.add_row("9. HERMES KANBAN DEMO VIDEO", str(kanban_video_path), "📋 ANIMATED MP4")
    table.add_row("10. Durable Hermes SQLite DB", "data/kanban.db", "💾 Persistent")

    console.print(table)


def run_full_pipeline(orchestrator: HermesWorkflowOrchestrator) -> None:
    """Run all 6 agents sequentially through Hermes Kanban stages."""
    console.print("\n[bold cyan]▶ STEP 1/6: Ads Manager Agent[/bold cyan]")
    ads_agent = AdsManagerAgent(orchestrator)
    ads_dataset = ads_agent.run(days_back=30)
    orchestrator.render_board()

    console.print("\n[bold cyan]▶ STEP 2/6: Marketing Analysis Agent[/bold cyan]")
    analysis_agent = MarketingAnalyzerAgent(orchestrator)
    analysis_report = analysis_agent.run(ads_dataset)
    orchestrator.render_board()

    console.print("\n[bold cyan]▶ STEP 3/6: Research Agent (Tavily/Exa + CWT Unique Data)[/bold cyan]")
    research_agent = ResearchAgent(orchestrator)
    research_report = research_agent.run()
    orchestrator.render_board()

    console.print("\n[bold cyan]▶ STEP 4/6: Script Agent (Generating 3 Distinct Storyboards)[/bold cyan]")
    script_agent = ScriptAgent(orchestrator)
    storyboards = script_agent.run(analysis_report, research_report)
    orchestrator.render_board()

    console.print("\n[bold cyan]▶ STEP 5/6: Creative Critic Agent (Scoring & Winner Selection)[/bold cyan]")
    critic_agent = CreativeCriticAgent(orchestrator)
    winner_sb, scores_report = critic_agent.run(storyboards)
    orchestrator.render_board()

    console.print(f"\n[bold green]🏆 Winner Selected: '{winner_sb.title}' (Score: {scores_report.evaluations[0].composite_score}/10)[/bold green]")

    console.print("\n[bold cyan]▶ STEP 6/6: Video Production Agent (Rendering 9:16 Ad & Kanban Video)[/bold cyan]")
    video_agent = VideoAgent(orchestrator)
    final_ad_path, kanban_video_path = video_agent.run(winner_sb)
    orchestrator.render_board()

    print_final_summary(final_ad_path, kanban_video_path)


def main():
    parser = argparse.ArgumentParser(description="CrowdWisdomTrading Hermes Video Ads Agent System")
    parser.add_argument("--demo", action="store_true", help="Force DEMO_MODE (offline with verified fixtures)")
    parser.add_argument("--full-run", action="store_true", help="Execute complete multi-agent pipeline")
    parser.add_argument("--ads-only", action="store_true", help="Run only the Ads Manager Agent")
    parser.add_argument("--analyze-only", action="store_true", help="Run Ads Manager + Marketing Analyzer")
    parser.add_argument("--research-only", action="store_true", help="Run Research Agent")
    parser.add_argument("--scripts-only", action="store_true", help="Run up to 3 storyboards generation")
    parser.add_argument("--critic-only", action="store_true", help="Run up to Creative Critic scoring")
    parser.add_argument("--video-only", action="store_true", help="Render video from selected storyboard")
    parser.add_argument("--kanban-board", action="store_true", help="Display Hermes Kanban board in terminal")
    parser.add_argument("--kanban-video", action="store_true", help="Render animated Hermes Kanban MP4 video")
    parser.add_argument("--debug", action="store_true", help="Enable verbose debug logging")

    args = parser.parse_args()

    if args.demo:
        settings.demo_mode = True

    settings.ensure_directories()
    setup_logging(args.debug or settings.debug_logging)
    print_banner()

    # Initialize Hermes Kanban Database & Orchestrator
    kanban_db = HermesKanbanDB(settings.kanban_db_path)
    viewer = HermesKanbanViewer(kanban_db)
    orchestrator = HermesWorkflowOrchestrator(kanban_db, viewer)

    if args.kanban_board:
        viewer.print_terminal_board(orchestrator.current_stage)
        return

    if args.kanban_video:
        out_v = settings.outputs_dir / "hermes_kanban_demo.mp4"
        console.print(f"[bold cyan]Rendering animated Hermes Kanban video to {out_v}...[/bold cyan]")
        viewer.render_kanban_video(out_v, duration_seconds=12)
        console.print(f"[bold green]Saved: {out_v}[/bold green]")
        return

    if args.ads_only:
        AdsManagerAgent(orchestrator).run()
        orchestrator.render_board()
        return

    if args.analyze_only:
        ads = AdsManagerAgent(orchestrator).run()
        MarketingAnalyzerAgent(orchestrator).run(ads)
        orchestrator.render_board()
        return

    if args.research_only:
        ResearchAgent(orchestrator).run()
        orchestrator.render_board()
        return

    if args.scripts_only:
        ads = AdsManagerAgent(orchestrator).run()
        ana = MarketingAnalyzerAgent(orchestrator).run(ads)
        res = ResearchAgent(orchestrator).run()
        ScriptAgent(orchestrator).run(ana, res)
        orchestrator.render_board()
        return

    if args.critic_only:
        ads = AdsManagerAgent(orchestrator).run()
        ana = MarketingAnalyzerAgent(orchestrator).run(ads)
        res = ResearchAgent(orchestrator).run()
        sbs = ScriptAgent(orchestrator).run(ana, res)
        CreativeCriticAgent(orchestrator).run(sbs)
        orchestrator.render_board()
        return

    if args.video_only:
        winner, _ = CreativeCriticAgent(orchestrator).run()
        video_agent = VideoAgent(orchestrator)
        final_ad_path, kanban_video_path = video_agent.run(winner)
        print_final_summary(final_ad_path, kanban_video_path)
        return

    # Default: Run full pipeline
    run_full_pipeline(orchestrator)


if __name__ == "__main__":
    main()
