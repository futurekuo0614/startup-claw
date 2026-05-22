# Startup Investment Intelligence Pipeline — STARTUP-CLAW

## System Overview
Python-based pipeline: Web Scraper → Google Sheets → LLM+ML Scoring → Firebase → Weekly Report Email

## Tech Stack
- Language: Python 3.12
- LLM: Qwen (via Ollama, local)
- Storage: Google Sheets (intermediate), Firebase (final output)
- APIs: gspread, firebase-admin, smtplib/Gmail API
- Config: .env (environment variables)
- Environment: GitHub Codespace

## Common Commands
```bash
# Run full pipeline
python main.py

# Run scraper only
python scraper.py

# Run AI scoring only
python ai_processor.py

# Run weekly report
python weekly_report.py

# Start Ollama
ollama serve
ollama run qwen


Project Structure

main.py — Orchestrates full pipeline
scraper.py — Scrapes startup investment news from web sources
ai_processor.py — Sends data to Qwen (via Ollama) + ML model, produces weighted scores
firebase_client.py — Pushes scored results to Firebase
weekly_report.py — Generates weekly summary report
config.py — Centralized configuration (API keys, paths, constants)
.env — Environment variables (secrets, credentials)
requirements.txt — Python dependencies
scraper.py.bak — Backup of previous scraper version

Data Flow (strict order)

scraper.py → raw news data (title, URL, content, funding round)
Raw data → Google Sheets (intermediate storage)
ai_processor.py reads Google Sheets → Qwen (summary, classification) + ML model (scoring)
Weighted score = f(LLM score, ML score) → final output
firebase_client.py → pushes to Firebase (summary, URL, funding round, company fit, score)
weekly_report.py → generates weekly report from Firebase data → email (planned)

Output Schema (Firebase)
Each record must include:

news_summary (LLM-generated)
source_url
funding_round
company_fit_score
overall_weighted_score
timestamp

Coding Rules
Rule 1 — Think before coding
State assumptions explicitly. If uncertain about my pipeline logic, ask. Don't guess data schemas.
Rule 2 — Simplicity first
No unnecessary abstractions. This is a data pipeline, not a framework.
Rule 3 — Surgical changes
Only modify what's directly related to the task. Don't refactor working scraper.py logic when fixing ai_processor.py.
Rule 4 — Goal-driven execution
Define success criteria before implementing. Run the pipeline end-to-end to verify.
Rule 5 — Use LLM only for judgment calls
Qwen handles: summarization, classification, company-fit assessment.
Qwen must NOT handle: retry logic, API routing, status-code decisions. Use plain Python for those.
Rule 6 — Token budgets matter
Qwen prompts should be concise. Batch requests when possible. If Ollama times out, log and retry with backoff — don't silently skip.
Rule 7 — Surface conflicts
If scraper.py output format conflicts with ai_processor.py input expectations, flag it. Don't silently transform.
Rule 8 — Read before you write
Before modifying any module, read its exports and callers. Understand the full data flow first.
Rule 9 — Tests verify intent
Tests must validate business logic (e.g., "high funding round + AI sector = higher fit score"), not just "function returns something."
Rule 10 — Checkpoint after every step
For multi-step refactors, report: what's done, what's verified, what's left.
Rule 11 — Match existing conventions
Follow the project's existing naming, error handling, and logging patterns in config.py.
Rule 12 — Fail loud
Never report "pipeline completed" if any step was skipped or errored silently. Surface all failures explicitly.
Prohibited Actions

Do NOT delete or overwrite existing Google Sheets data without confirmation
Do NOT push to Firebase without validating score ranges (0-100)
Do NOT hardcode API keys — use .env + config.py
Do NOT introduce new dependencies without stating why
Do NOT modify scraper.py.bak (it's a backup)