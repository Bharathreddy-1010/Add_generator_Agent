# Internship Assessment Submission Checklist
**Candidate Assessment**: CrowdWisdomTrading AI Marketing Video Ads Hermes Agent  
**Position**: Marketing Lead using AI Agents  
**Reviewer / CEO**: Gilad Bar-Ilan (gilad@crowdwisdomtrading.com)

---

## 1. Required Deliverables Matrix

| Requirement | Project Implementation | Location / Status |
| :--- | :--- | :--- |
| **1. GitHub/GitLab Repository** | Clean git-ready codebase with `.gitignore`, `requirements.txt`, clean modular architecture | `/Users/bharathreddy/Desktop/CWT_project` |
| **2. Apify Meta Ads Scraping** | Live client + 30-day filter + raw response logging + normalized JSON | `tools/apify_client.py`<br>`data/ads/winning_ads.json` |
| **3. Tavily / Exa Research** | 30-day recency search on Reddit/FinTwit retail trader pain points | `tools/tavily_client.py`<br>`data/research/icp_pain_research.json` |
| **4. Hermes Agent Framework & Kanban** | Durable SQLite-backed Kanban task board + state transitions | `hermes/kanban_db.py`<br>`data/kanban.db` |
| **5. Video Output of Hermes Kanban** | Animated 1920x1080 MP4 showing Kanban task transitions | `outputs/hermes_kanban_demo.mp4` |
| **6. 3 Distinct Storyboards** | 1. Pain+ICP, 2. Unique Data, 3. CWT Decision-Making | `data/scripts/storyboard_1.json`<br>`data/scripts/storyboard_2.json`<br>`data/scripts/storyboard_3.json` |
| **7. Creative Critic Scoring** | 10 performance-marketing criteria evaluated 1-10 with selection rationale | `data/analysis/concept_scores.json` |
| **8. "WOW" Final Video Ad** | 9:16 vertical 1080x1920 MP4 ad with voiceover, kinetic graphics & sound | `outputs/final_ad.mp4` |
| **9. Re-runnable Without Paid Account Burn** | Complete `DEMO_MODE=true` offline support using verified fixtures | `python main.py --demo` |

---

## 2. Fast Verification Commands
```bash
# 1. Activate environment
source .venv/bin/activate

# 2. Run full pipeline end-to-end (Demo Mode)
python main.py --demo

# 3. View Hermes Terminal Kanban Board
python main.py --kanban-board

# 4. Run automated test suite
pytest -v tests/
```
