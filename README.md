# CrowdWisdomTrading AI Marketing Video Ads Agent (Hermes Framework)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Hermes Kanban](https://img.shields.io/badge/Orchestrator-Hermes%20Kanban-cyan.svg)](https://github.com/NousResearch/hermes-agent)
[![Remotion / OpenMontage](https://img.shields.io/badge/Engine-OpenMontage%20Remotion-purple.svg)](https://github.com/calesthio/OpenMontage)
[![Design Style](https://img.shields.io/badge/Style-Vox%20Master%20Sheet-red.svg)](https://remotion.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

An autonomous multi-agent performance marketing and video production system built for **[CrowdWisdomTrading](https://crowdwisdomtrading.com)** as part of the Marketing Lead AI Agent Internship Assessment (CEO: Gilad Bar-Ilan, `gilad@crowdwisdomtrading.com`).

The system uses the **Hermes multi-agent orchestration framework** to research successful competitor financial ads, extract core psychological hooks, identify current retail trader pain points, draft 3 distinct video-ad storyboards, objectively evaluate them across 10 performance marketing dimensions, and produce a broadcast-grade **30–60 second 9:16 vertical video ad** following the authentic **Vox Style Master Sheet** aesthetic, alongside an **animated MP4 video of the Hermes Kanban workflow**.

---

## Assessment Deliverables Summary

All requirements from the 2-page assessment specification are implemented and verified:

| Assessment Requirement | Technical Implementation | Output Deliverables & Locations | Status |
| :--- | :--- | :--- | :--- |
| **1. Python Project & Hermes Framework** | Multi-agent orchestration engine with ACID SQLite Kanban state tracking | `hermes/workflow.py`<br>`data/kanban.db` | ✅ Complete |
| **2. LLM Provider (OpenRouter / NVIDIA NIM)** | `StructuredLLMClient` supporting OpenRouter and NVIDIA NIM API endpoints | `tools/llm_client.py`<br>`config/settings.py` | ✅ Complete |
| **3. Apify Meta Ads Scraping (<= 30 Days)** | Scrapes Meta Ad Library via Apify, normalizes fields, filters 30-day window | `tools/apify_client.py`<br>`data/ads/winning_ads.json` | ✅ Complete |
| **4. Marketing & Concept Extraction** | Extracts psychological hooks, pain points, ICP targets, and CWT counter-angles | `agents/marketing_analyst.py`<br>`data/analysis/marketing_analysis.json` | ✅ Complete |
| **5. 3 Storyboard Types via Tavily/Exa** | 1. Pain+ICP (Solo Trader Trap)<br>2. Unique CWT Data (78% Reversal Signal)<br>3. CWT Decision-Making (Execution Cockpit) | `agents/script_agent.py`<br>`data/scripts/storyboard_1.json`<br>`data/scripts/storyboard_2.json`<br>`data/scripts/storyboard_3.json` | ✅ Complete |
| **6. Creative Critic Selection** | 10-metric weighted scoring model selecting the highest-converting concept | `agents/creative_critic.py`<br>`data/analysis/concept_scores.json` | ✅ Complete |
| **7. 30–60s "WOW" Video Ad (OpenMontage)** | 1080x1920 9:16 Vox-style ad with neural male narration & karaoke subtitles | `tools/openmontage_renderer.py`<br>[outputs/final_ad.mp4](file:///Users/bharathreddy/Desktop/CWT_project/outputs/final_ad.mp4) | ✅ Complete |
| **8. Animated Hermes Kanban Video** | 1080x1920 MP4 video demonstrating real-time Kanban stage progression | `hermes/kanban_view.py`<br>[outputs/hermes_kanban_demo.mp4](file:///Users/bharathreddy/Desktop/CWT_project/outputs/hermes_kanban_demo.mp4) | ✅ Complete |
| **9. Re-runnable Without Burning Paid Accounts** | Fully functional offline `DEMO_MODE=true` with verified production fixtures | `python main.py --demo` | ✅ Complete |
| **10. Automated Test Suite** | 10 comprehensive unit tests covering schemas, normalization, scoring, and video | `pytest tests/` | ✅ 100% Pass |

---

## System Architecture

```
                    ┌─────────────────────────────────────────┐
                    │      CrowdWisdomTrading Platform        │
                    │       (crowdwisdomtrading.com)          │
                    └────────────────────┬────────────────────┘
                                         │
                    ┌────────────────────▼────────────────────┐
                    │      Hermes Kanban Orchestrator         │
                    │           (data/kanban.db)              │
                    └────────────────────┬────────────────────┘
                                         │
       ┌─────────────────────────────────┴─────────────────────────────────┐
       ▼                                                                   ▼
┌───────────────────────────────┐                   ┌───────────────────────────────┐
│ 1. Ads Manager Agent          │                   │ 2. Marketing Analysis Agent   │
│ - Apify Meta Ads Scraper      │                   │ - Hook & Pain Decomposition   │
│ - 30-Day Recency Filter       ├──────────────────►│ - Emotional Triggers          │
│ - Normalized Dataset (JSON)   │                   │ - CWT Counter-Positioning     │
└───────────────────────────────┘                   └───────────────┬───────────────┘
                                                                    │
                                                                    ▼
                                                    ┌───────────────────────────────┐
                                                    │ 3. Research Agent             │
                                                    │ - Tavily / Exa 30-Day Search  │
                                                    │ - Retail Reddit / FinTwit     │
                                                    │ - CWT Unique Data Metrics     │
                                                    └───────────────┬───────────────┘
                                                                    │
                                                                    ▼
                                                    ┌───────────────────────────────┐
                                                    │ 4. Script Agent               │
                                                    │ - Storyboard 1: Pain + ICP    │
                                                    │ - Storyboard 2: Unique Data   │
                                                    │ - Storyboard 3: Decision Flow │
                                                    └───────────────┬───────────────┘
                                                                    │
                                                                    ▼
                                                    ┌───────────────────────────────┐
                                                    │ 5. Creative Critic Agent      │
                                                    │ - 10-Metric Weighted Scoring  │
                                                    │ - Selection & Rationale       │
                                                    │ - Scene Timing Refinement     │
                                                    └───────────────┬───────────────┘
                                                                    │
                                                                    ▼
                                                    ┌───────────────────────────────┐
                                                    │ 6. Video Production Agent     │
                                                    │ - OpenMontage Remotion Engine │
                                                    │ - Vox Style Master Sheet UI   │
                                                    │ - Interactive Male Neural TTS │
                                                    │ - Real-Time Karaoke Subtitles │
                                                    │ - Frame-Accurate Audio Sync   │
                                                    └───────────────┬───────────────┘
                                                                    │
                                    ┌───────────────────────────────┴───────────────────────────────┐
                                    ▼                                                               ▼
                     outputs/final_ad.mp4                                            outputs/hermes_kanban_demo.mp4
           (1080x1920 Vox Performance Video Ad)                            (Hermes Kanban Animated Video Submission)
```

---

## Visual Aesthetics: Vox Style Master Sheet

The video ad engine strictly adheres to the reference **"VOX STYLE MASTER SHEET - VISUAL SYSTEM FOR A DOCUMENTARY-COLLAGE EXPLAINER SERIES"**:

| Master Sheet Token | Hex Code | Visual Implementation |
| :--- | :--- | :--- |
| **Archival Tan** | `#C9BB9C` | Archival paper canvas background with halftone dot grid texture and subtle drifting coordinates. |
| **Ink Black** | `#1A1A1A` | High-contrast typography (`Impact`, `Courier New`, `Inter`), card keylines, and sharp sticker drop frames. |
| **Hot Red** | `#B62E1F` | Reserved strictly for sticker offset drop shadows (`6px 6px 0px #B62E1F`), directional arrows, stat accents, and real-time word karaoke highlights. |
| **Mustard** | `#D9A441` | Secondary newsroom accent reserved for `Fig. X - [Label]` typewriter metadata badges. |
| **Paper White** | `#F8F5EE` | Clean archival cutout cards with crisp borders. |

### Visual Scene Progression (Storyboard 2: The 78% Reversal Signal)
- **Scene 1: The Retail Trap** — Vintage trader cutout with sticker border, directional arrow, and hero 84% buying conviction counter.
- **Scene 2: 76% Institutional Divergence** — Animated SPY divergence curve showing institutional short turns while retail hype climbed, with map pin dropping at peak (-3.8% drop).
- **Scene 3: 16,420+ Sources Monitored** — Newsroom feed cards cascading for YouTube Channel Transcripts, Reddit Sentiment Signals, and FinTwit Institutional Streams.
- **Scene 4: Verified Track Record** — Founder Gilad Bar-Ilan (25+ years experience) credential badge alongside verified execution levels (Entry $482.50, Target $488.20, Stop $479.80).
- **Scene 5: Stop Being Exit Liquidity** — Split comparison cards contrasting "Chasing Social Hype" vs "Trade the Reaction" with 1:3 risk/reward.
- **Scene 6: Get 20 Free Predictions** — Newsroom finale CTA with feature checklist and pulsing `START AT CROWDWISDOMTRADING.COM` button.

---

## Audio & Video Synchronization Engine

To guarantee 100% audio-visual synchronization without latency or drift:

1. **Trailing Dead Silence Elimination**: Neural TTS engines append ~1.0–1.2 seconds of trailing silence. Our engine implements `_trim_trailing_silence` in `tools/tts_engine.py`, detecting actual speech completion over 50ms energy windows and retaining a natural 0.25s breath cushion. Scene transitions snap instantly when the sentence finishes.
2. **Per-Sequence Audio Binding**: Each scene's audio file (`assets/vox_scene_01.wav` through `06.wav`) is mounted directly inside its respective Remotion `<Sequence>`, ensuring zero cumulative drift across cuts.
3. **Real-Time Karaoke Subtitles**: `VoxCaptionOverlay` calculates word timings based on character weights across the active speaking window. The active word illuminates in real time in a **Hot Red pill badge (`#B62E1F`)** with white text.
4. **Interactive Male Neural Voice**: Uses Microsoft Edge Neural TTS `en-US-ChristopherNeural` (natural marketing delivery, authoritative inflection) with graceful fallback to macOS male voices (`Daniel` / `Alex`).

---

## Installation & Quickstart

### Prerequisites
- Python 3.10+
- Node.js 18+ (for Remotion video rendering)
- FFmpeg (installed via `brew install ffmpeg` on macOS or `apt install ffmpeg` on Linux)

### 1. Setup Virtual Environment
```bash
# Clone the repository
git clone https://github.com/your-username/CWT_project.git
cd CWT_project

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Install Remotion dependencies
cd remotion-composer
npm install
cd ..
```

### 2. Configure Environment Variables
```bash
cp .env.example .env
```
Edit `.env` to configure your API keys:
```ini
# Run offline using verified fixtures (ideal for evaluators to avoid burning credits)
DEMO_MODE=true

# LLM Configuration (OpenRouter or NVIDIA NIM)
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=your_openrouter_key
OPENROUTER_MODEL=meta-llama/llama-3.3-70b-instruct

# Data Scraping & Search APIs
APIFY_API_TOKEN=your_apify_token
TAVILY_API_KEY=your_tavily_key
EXA_API_KEY=your_exa_key

# Video & Voiceover
VIDEO_RESOLUTION_WIDTH=1080
VIDEO_RESOLUTION_HEIGHT=1920
VIDEO_FPS=30
VOICEOVER_ENABLED=true
VOICEOVER_VOICE=en-US-ChristopherNeural
```

---

## Execution Commands

### Run Full Pipeline End-to-End
```bash
# Recommended for evaluators: Run full pipeline end-to-end in Demo Mode (zero account burn)
python main.py --demo

# Run full pipeline with live external APIs (Apify + Tavily/Exa + OpenRouter/NVIDIA)
python main.py --full-run
```

### Run Individual Agent Stages
```bash
python main.py --ads-only        # Stage 1: Apify Meta Ads extraction & normalization
python main.py --analyze-only    # Stage 2: Marketing strategy & hook analysis
python main.py --research-only   # Stage 3: Tavily/Exa ICP pain point research
python main.py --scripts-only    # Stage 4: Generate 3 distinct video-ad storyboards
python main.py --critic-only     # Stage 5: Creative Critic 10-metric evaluation
python main.py --video-only      # Stage 6: Render Vox Explainer 9:16 MP4 ad
```

### View Hermes Kanban Board
```bash
# View interactive ASCII/Rich Hermes Kanban board in terminal
python main.py --kanban-board

# Render standalone animated MP4 video of the Hermes Kanban board
python main.py --kanban-video
```

---

## Output Artifacts & Project Structure

```
CWT_project/
├── agents/                       # Hermes multi-agent implementations
│   ├── ads_manager.py            # Stage 1: Apify Meta Ads extraction
│   ├── marketing_analyst.py      # Stage 2: Strategy, pain & hook deconstruction
│   ├── research_agent.py         # Stage 3: Tavily/Exa 30-day retail pain research
│   ├── script_agent.py           # Stage 4: 3 distinct storyboard concepts
│   ├── creative_critic.py        # Stage 5: 10-metric weighted evaluation
│   └── video_agent.py            # Stage 6: Video production orchestrator
├── data/                         # Intermediate JSON artifacts & SQLite DB
│   ├── ads/
│   │   ├── raw/                  # Raw Apify response archives
│   │   └── winning_ads.json      # Filtered 30-day winning ad records
│   ├── analysis/
│   │   ├── marketing_analysis.json # Psychological hooks, ICP & CWT angles
│   │   └── concept_scores.json   # Creative Critic 10-metric evaluation
│   ├── research/
│   │   └── icp_pain_research.json# 30-day Reddit/FinTwit retail pain findings
│   ├── scripts/
│   │   ├── storyboard_1.json     # Concept 1: Pain + ICP (Solo Trader Trap)
│   │   ├── storyboard_2.json     # Concept 2: Unique Data (78% Reversal Signal)
│   │   └── storyboard_3.json     # Concept 3: CWT Decision Value (Cockpit)
│   ├── crowdwisdom/              # Authentic CWT product intelligence & stats
│   └── kanban.db                 # Persistent SQLite database for Hermes Kanban
├── hermes/                       # Hermes workflow & Kanban task management
│   ├── workflow.py               # Multi-agent stage controller & audit logger
│   ├── kanban_db.py              # SQLite ACID task repository
│   └── kanban_view.py            # Terminal board viewer & MP4 video generator
├── remotion-composer/            # OpenMontage Remotion React Video Engine
│   ├── src/
│   │   ├── VoxExplainer.tsx      # Vox Style Master Sheet composition
│   │   └── components/
│   │       └── VoxCollage.tsx    # Sticker borders, arrows, stat cards
│   └── public/demo-props/        # Remotion cut definitions & timing JSON
├── tools/                        # API clients & rendering utilities
│   ├── apify_client.py           # Meta Ad Library scraper client
│   ├── tavily_client.py          # Tavily search client (30-day filter)
│   ├── exa_client.py             # Exa search client
│   ├── llm_client.py             # OpenRouter & NVIDIA NIM LLM client
│   ├── openmontage_renderer.py   # OpenMontage Remotion render bridge
│   ├── video_renderer.py         # Secondary native OpenCV 9:16 renderer
│   └── tts_engine.py             # Microsoft Edge neural TTS & silence trimmer
├── tests/                        # Automated unit & integration tests
│   ├── test_schemas.py           # Pydantic schema validation tests
│   ├── test_ads_normalization.py # 30-day filtering & normalization tests
│   ├── test_scoring.py           # Creative Critic 10-metric scoring tests
│   ├── test_storyboard_validation.py # Scene timing & hook validation tests
│   ├── test_kanban_workflow.py   # SQLite Kanban state transition tests
│   ├── test_openmontage.py       # OpenMontage props & timing tests
│   └── test_video_renderer.py    # Voiceover synthesis & video render tests
└── outputs/                      # Final Rendered Media Deliverables
    ├── final_ad.mp4              # 🎬 1080x1920 9:16 Vox Performance Video Ad
    ├── final_ad_vertical.mp4     # 🎬 1080x1920 Vertical Edition
    └── hermes_kanban_demo.mp4    # 📋 Animated Hermes Kanban MP4 Video
```

---

## Automated Testing

Run the full pytest suite:
```bash
pytest -v tests/
```

All 10 unit tests pass with 100% success rate:
- `test_schemas.py`: Validates Pydantic data schemas for ads, research, storyboards, and Kanban tasks.
- `test_ads_normalization.py`: Validates Apify ad normalization, field mapping, and 30-day date cutoff.
- `test_scoring.py`: Validates 10-metric weighted scoring math and winner selection logic.
- `test_storyboard_validation.py`: Validates scene count, duration boundaries (30–60s), and visual hooks.
- `test_kanban_workflow.py`: Validates SQLite ACID operations and task stage transitions.
- `test_openmontage.py`: Validates Remotion props generation and cut duration math.
- `test_video_renderer.py`: Validates TTS voiceover synthesis and silence trimming.

---

## Financial Advertising Compliance & Guardrails

This system enforces strict ethical financial advertising standards:
- **No Guaranteed Returns**: Promises of "guaranteed returns", "100% win rate", or "zero risk" are strictly blocked.
- **Empirical Probability Grounding**: Ads are anchored in mathematical edge, crowd divergence statistics, and disciplined stop-loss risk management.
- **Clear Disclaimers**: Content is framed as educational market intelligence and decision support.
