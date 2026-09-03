# AGENTS.md

## Project purpose and stack
This repository is the course Task Tracker application. It uses Python 3.10+ with FastAPI, Pydantic, Uvicorn, a JSON-file repository, pytest/httpx tests, and a static HTML/JavaScript Kanban frontend.

## Read first
Before proposing or applying a change, read the relevant existing files and the matching course evidence under `docs/`. Preserve the current layered flow: API route -> service -> repository -> JSON storage. Do not bypass the service/repository layers from API routes.

## Run and test commands
- Local API: `python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000`
- Tests: `python -m pytest tests/ -q`
- Health check: `curl http://127.0.0.1:8000/health`
- Docker build: `docker build -t task-tracker .`
- Docker run: `docker run --rm -p 8000:8000 task-tracker`
- Docker health check: `curl http://127.0.0.1:8000/health`

## Final-project guardrails
1. Do not add new product features for the final project. The final work is release-readiness, verification, documentation, CI, Docker, security review, and ownership evidence.
2. Treat `app/` and `frontend/` as protected. Change them only for a small verified bug fix, security fix, or documentation-supported correction. Explain any such final-project edit in `docs/final-ai-review.md`.
3. Do not paste, commit, or generate real credentials, tokens, `.env` values, production logs, or real customer/patient/personal data.
4. Never weaken tests or CI to make a build green. Do not use `continue-on-error`, `|| true`, skipped pytest commands, or other failure-hiding shortcuts.
5. Keep `is_overdue` derived rather than persisted, preserve the existing status-transition rules, and keep tests isolated from `app/data/tasks.json` through `TASKS_FILE`.
6. Review every AI-generated diff before keeping it. If a changed line or command cannot be explained, do not submit it.
7. Verify factual documentation claims against the repository or a real command result. Record uncertainty instead of inventing evidence.

## Review expectations
For code changes, inspect the diff, run the smallest relevant tests, then run the full suite. For release/config changes, verify exact commands and check for accidental secret inclusion. AI review findings must be graded rather than accepted automatically.
