# CrowdWisdomTrading AI Marketing Video Ads Agent System
## Architecture & Technical Specification

### 1. System Overview
This project is an autonomous, multi-agent AI performance marketing system designed for **CrowdWisdomTrading (CWT)**. It researches competitor advertising, extracts deep psychological hooks and market gaps, gathers fresh market intelligence, generates 3 distinct video-ad storyboards, scores them objectively, and produces a final 9:16 vertical video advertisement alongside an animated video of the Hermes Kanban workflow.

### 2. Multi-Agent Architecture

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

### 3. Hermes Kanban State Machine
The system adheres to the Nous Research Hermes Agent task board architecture, backed by a persistent SQLite database (`data/kanban.db`):
- **Tables**: `boards`, `tasks`, `task_events`.
- **Stages**:
  1. `RESEARCHING_ADS`: Scraping Meta ad library.
  2. `ANALYZING_ADS`: Deconstructing competitor strategy without copying.
  3. `RESEARCHING_ICP`: Investigating active trader pain points with 30-day recency.
  4. `GENERATING_SCRIPTS`: Generating 3 distinct 30-45s vertical storyboards.
  5. `EVALUATING_CONCEPTS`: Multi-criteria scoring and winner selection.
  6. `GENERATING_VIDEO`: Rendering final MP4 and animated Kanban video.
  7. `COMPLETED`: Finished state with all human-readable JSON and video outputs.

---

### 4. Financial Marketing & Anti-Hallucination Guardrails
- **Zero Profit Guarantees**: Strictly prohibited from promising "guaranteed profits", "100% win rates", or "risk-free trading".
- **Empirical Grounding**: Grounded in authentic CrowdWisdomTrading assets (Gilad Bar-Ilan 25-year pedigree, 16,420+ trader consensus points, defined risk invalidation levels).
- **Graceful Fallbacks**: If external APIs lack tokens or fail, the system transitions to verified local fixture datasets and clearly labels the output.
