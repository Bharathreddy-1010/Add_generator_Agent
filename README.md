# CrowdWisdomTrading AI Marketing Video Ads Hermes Agent System

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Hermes Kanban](https://img.shields.io/badge/Orchestrator-Hermes%20Kanban-cyan.svg)](https://github.com/NousResearch/hermes-agent)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

An autonomous multi-agent performance marketing and video ad production system built for **[CrowdWisdomTrading](https://crowdwisdomtrading.com)**.

The system researches competitor advertising in the financial trading niche, extracts core psychological hooks and market gaps, gathers fresh market intelligence, drafts 3 distinct video-ad storyboards, objectively evaluates them across 10 marketing dimensions, and automatically produces a high-impact 9:16 vertical video advertisement alongside an animated video of the Hermes Kanban workflow.

---

## Architecture

```
                    ┌─────────────────────────┐
                    │   CrowdWisdomTrading    │
                    └────────────┬────────────┘
                                 │
                   ┌─────────────▼─────────────┐
                   │  Hermes Kanban Engine     │
                   │    (data/kanban.db)       │
                   └─────────────┬─────────────┘
                                 │
      ┌──────────────────────────┴──────────────────────────┐
      ▼                                                     ▼
┌───────────────────────────┐                 ┌───────────────────────────┐
│ 1. Ads Manager Agent      │                 │ 2. Marketing Analysis     │
│ - Apify Meta Ads Scraper  │                 │ - Hook & Pain Extraction  │
│ - 30-Day Recency Filter   ├────────────────►│ - Emotional Triggers      │
│ - Normalized Dataset      │                 │ - CWT Adaptation Strategy │
└───────────────────────────┘                 └─────────────┬─────────────┘
                                                            │
                                                            ▼
                                              ┌───────────────────────────┐
                                              │ 3. Research Agent         │
                                              │ - Tavily / Exa 30d Search │
                                              │ - Retail Reddit / FinTwit │
                                              │ - CWT Unique Data Metrics │
                                              └─────────────┬─────────────┘
                                                            │
                                                            ▼
                                              ┌───────────────────────────┐
                                              │ 4. Script Agent           │
                                              │ - Storyboard 1 (Pain/ICP) │
                                              │ - Storyboard 2 (Data)     │
                                              │ - Storyboard 3 (Decision) │
                                              └─────────────┬─────────────┘
                                                            │
                                                            ▼
                                              ┌───────────────────────────┐
                                              │ 5. Creative Critic Agent  │
                                              │ - 10-Metric Weighted Eval │
                                              │ - Objective Winner Choice │
                                              │ - Scene Polish & Timing   │
                                              └─────────────┬─────────────┘
                                                            │
                                                            ▼
                                              ┌───────────────────────────┐
                                              │ 6. Video Production Agent │
                                              │ - 1080x1920 9:16 Vertical │
                                              │ - Kinetic Vox-Style UI    │
                                              │ - Synchronized Voiceover  │
                                              │ - FFmpeg Composition      │
                                              └─────────────┬─────────────┘
                                                            │
                                    ┌───────────────────────┴───────────────────────┐
                                    ▼                                               ▼
                      outputs/final_ad.mp4                            outputs/hermes_kanban_demo.mp4
                     (Performance Video Ad)                          (Kanban Video Submission)
```

---

## Agent Descriptions

| Agent | Responsibility | Output Artifact |
| :--- | :--- | :--- |
| **1. Ads Manager Agent** | Searches & extracts active financial ads via Apify Meta Ad Library actor (<= 30 days old). Normalizes fields, removes duplicates, and scores relevance. | `data/ads/winning_ads.json`<br>`data/ads/raw/` |
| **2. Marketing Analysis Agent** | Deconstructs competitor ads without copying. Identifies target ICPs, pain points, emotional triggers, offers, objections, and creative patterns. | `data/analysis/marketing_analysis.json` |
| **3. Research Agent** | Searches Reddit, FinTwit, and market journals using Tavily/Exa with 30-day recency. Fuses findings with authentic CrowdWisdom proprietary data. | `data/research/icp_pain_research.json` |
| **4. Script Agent** | Generates 3 radically distinct 30–45s video-ad storyboards (Pain+ICP, Unique Data, CWT Decision-Making) with scene-by-scene instructions and visual hooks. | `data/scripts/storyboard_1.json`<br>`data/scripts/storyboard_2.json`<br>`data/scripts/storyboard_3.json` |
| **5. Creative Critic Agent** | Evaluates all 3 storyboards across 10 performance marketing metrics (1–10 scale). Selects winner and refines scene cues. | `data/analysis/concept_scores.json` |
| **6. Video Production Agent** | Composes scenes, kinetic typography, charts, synchronized voiceover audio, and ambient soundscape into an MP4 video ad and animated Kanban MP4. | `outputs/final_ad.mp4`<br>`outputs/hermes_kanban_demo.mp4` |

---

## Installation & Setup

### Prerequisites
- Python 3.10+
- FFmpeg (installed via `brew install ffmpeg` on macOS or `apt install ffmpeg` on Linux)

### Setup Environment
```bash
# Clone the repository
git clone https://github.com/your-username/CWT_project.git
cd CWT_project

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Configuration & Environment Variables

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Key variables:
```ini
# Set to 'true' to run fully offline using verified fixtures (ideal for evaluators)
# Set to 'false' to call external live APIs
DEMO_MODE=true

# LLM Provider ('openrouter' or 'nvidia')
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=your_openrouter_key
OPENROUTER_MODEL=meta-llama/llama-3.3-70b-instruct

# NVIDIA Build alternative (https://build.nvidia.com/)
NVIDIA_API_KEY=your_nvidia_key
NVIDIA_MODEL=meta/llama-3.3-70b-instruct

# Data Scraping & Search APIs
APIFY_API_TOKEN=your_apify_token
TAVILY_API_KEY=your_tavily_key
EXA_API_KEY=your_exa_key

# Video & Voiceover
VIDEO_RESOLUTION_WIDTH=1080
VIDEO_RESOLUTION_HEIGHT=1920
VIDEO_FPS=30
VOICEOVER_ENABLED=true
VOICEOVER_VOICE=Samantha
```

---

## How External Integrations Work

### 1. Apify Meta Ads Integration
The `ApifyMetaAdsClient` triggers Meta Ad Library actors on Apify, retrieving active ad records from top financial tools (TradingView, Benzinga, TrendSpider). It filters records strictly to the last 30 days, normalizes headlines and copy, computes hook strength, and writes raw logs to `data/ads/raw/` and curated winning ads to `data/ads/winning_ads.json`.

### 2. Tavily & Exa Research Integration
The `TavilySearchClient` conducts targeted web searches with recency filters set to `days=30` and `search_depth="advanced"`. It pulls recent retail trader discussions from `r/Daytrading`, `r/stocks`, and FinTwit. Findings are mapped to `ResearchItem` schemas and stored in `data/research/icp_pain_research.json`.

### 3. Hermes Kanban Orchestration
The Hermes Kanban engine maintains persistent, ACID-compliant project states inside SQLite (`data/kanban.db`), storing tasks, event histories, and board states. It tracks tasks through verified transitions (`TODO` ➔ `IN_PROGRESS` ➔ `DONE`) and provides:
- Live terminal dashboards (`python main.py --kanban-board`)
- Automated animated MP4 video generation (`outputs/hermes_kanban_demo.mp4`) fulfilling the assessment submission requirement.

### 4. Video Production Engine
Due to OpenMontage requiring a full React/Remotion + Node.js 18+ multi-service repo, our system implements the OpenMontage pipeline principles natively in Python using FFmpeg 8.1.1, Pillow, OpenCV, and speech synthesis:
- **Kinetic Graphics**: 1080x1920 9:16 vertical resolution with animated split-screen comparisons, divergence charts, and consensus meters.
- **Synchronized Voiceover**: Generates audio narration matching each scene's exact duration.
- **Audio Ducking**: Combines voiceover with a background ambient music bed (ducked to 12% volume under speech).
- **H.264/AAC Export**: Produces high-quality, social-feed-ready video ads in `outputs/final_ad.mp4`.

---

## CLI Usage & Commands

```bash
# Run complete multi-agent pipeline end-to-end in Demo Mode (Recommended for evaluation)
python main.py --demo

# Run with live APIs (requires keys in .env)
python main.py --full-run

# Run individual agent stages
python main.py --ads-only        # Run only Ads Manager Agent
python main.py --analyze-only    # Run Ads Manager + Marketing Analyzer
python main.py --research-only   # Run Research Agent
python main.py --scripts-only    # Run up to 3 storyboards generation
python main.py --critic-only     # Run up to Creative Critic evaluation
python main.py --video-only      # Render final MP4 from winning concept

# View Hermes Kanban task board in terminal
python main.py --kanban-board

# Render standalone Hermes Kanban animated MP4 video
python main.py --kanban-video
```

---

## Output Structure

```
data/
├── ads/
│   ├── raw/                       # Raw API responses
│   └── winning_ads.json           # Filtered 30-day winning ads
├── analysis/
│   ├── marketing_analysis.json    # Hook, pain, and adaptation report
│   └── concept_scores.json        # 10-metric Creative Critic evaluation
├── research/
│   └── icp_pain_research.json     # 30-day fresh market research findings
├── scripts/
│   ├── storyboard_1.json          # Concept 1: Pain + ICP (Solo Trader Trap)
│   ├── storyboard_2.json          # Concept 2: Unique Data (78% Reversal Signal)
│   └── storyboard_3.json          # Concept 3: CWT Decision Value (Execution Cockpit)
├── crowdwisdom/                   # Authentic CWT product & unique data
└── kanban.db                      # Persistent Hermes SQLite task database

outputs/
├── assets/                        # Individual scene frames, waveforms, audio files
├── renders/                       # Individual scene MP4 renders
├── final_ad.mp4                   # 🎬 30-45s 9:16 Vertical Video Advertisement
└── hermes_kanban_demo.mp4         # 📋 Animated Hermes Kanban Board MP4 Video
```

---

## Financial Advertising Compliance & Safety

This project strictly enforces ethical financial advertising standards:
- **No Guaranteed Returns**: Promising "guaranteed profit", "100% win-rate", or "risk-free" returns is strictly blocked.
- **Empirical Grounding**: Ads are anchored in realistic probabilities, sentiment divergence, and risk management.
- **Clear Disclaimers**: Content is framed as market intelligence and educational research support.

---

## Automated Testing

Run the full pytest test suite:
```bash
pytest -v tests/
```

Test coverage includes:
1. Pydantic schema validation (`test_schemas.py`)
2. Ad normalization, deduplication, and 30-day filtering (`test_ads_normalization.py`)
3. Creative Critic 10-metric weighted scoring (`test_scoring.py`)
4. Storyboard scene timing and sequence integrity (`test_storyboard_validation.py`)
5. Hermes SQLite Kanban persistence and audit trails (`test_kanban_workflow.py`)
6. Voiceover synthesis and audio generation (`test_video_renderer.py`)

---

## Submission Notes
For review by Gilad Bar-Ilan (`gilad@crowdwisdomtrading.com`):
- All required deliverables are implemented and runnable.
- `outputs/final_ad.mp4` contains the complete high-impact 9:16 vertical video ad.
- `outputs/hermes_kanban_demo.mp4` contains the animated Hermes Kanban video capture.
