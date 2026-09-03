# Release Evidence

## Baseline
- Branch required for final submission: `final-project`.
- Date checked: 2026-09-02.
- Local app run command: `python -m uvicorn app.main:app --host 127.0.0.1 --port 8765`.
- `/health` result: HTTP `200 OK` with JSON `{"status":"ok", ...}` on 2026-09-03.
- Frontend check: **PASS**. On 2026-09-03, the application was started locally on port 8000 and opened at `http://localhost:8000/`. The Kanban board loaded successfully with tasks visible in the To Do, In Progress, and Done columns. The create flow was verified by creating `Final frontend test`, and the edit flow was verified by changing its title to `Final frontend test edited`.
- Test command: `python -m pytest tests/ -q`.
- Test result: `45 passed, 4 warnings in 0.26s`.

## CI evidence
- Workflow file: `.github/workflows/ci.yml`.
- Trigger: push and pull request.
- Python version: `3.11`.
- Dependency installation: installs `requirements.txt`, then `pytest` and `httpx` required by the test suite.
- Test command used by CI: `python -m pytest tests/ -q`.
- Shortcut check: no `continue-on-error`, no `|| true`, pytest is not skipped, and dependency installation is explicit.
- Latest GitHub Actions status: **PASS**.
- Branch tested: `final-project`.
- Latest successful run: Update final AI review evidence.
- Result: 45 passed, 4 warnings in 0.26s.

## Docker evidence
- Dockerfile: `Dockerfile`.
- Ignore file: `.dockerignore`.
- Build command: `docker build -t task-tracker .`.
- Run command: `docker run -d --name task-tracker-final -p 8000:8000 task-tracker`.
- Container health command: `curl -i http://127.0.0.1:8000/health`.
- Expected result from application contract: HTTP `200` and a JSON body with `status: "ok"` and a timestamp.
- Non-root check: the Dockerfile creates `appuser` and switches to `USER appuser` before runtime.
- No-baked-secrets check: `.dockerignore` excludes `.env` and `.env.*`; only the application and frontend are copied after dependency installation.
- Docker runtime verification: **PASS** on 2026-09-03 using GitHub Codespaces.
- Docker image build: **PASS** using `docker build -t task-tracker .`.
- Container run: **PASS** using `docker run -d --name task-tracker-final -p 8000:8000 task-tracker`.
- Container `/health` verification: **PASS**. `curl -i http://localhost:8000/health` returned `HTTP/1.1 200 OK` with JSON containing `"status":"ok"`.

## Documentation claim-vs-reality log

| Claim checked | Evidence used | Result | Change made, if any |
|---|---|---|---|
| The full test suite passes. | `python -m pytest tests/ -q` | PASS: 45 passed, 4 warnings in 0.26s | README Final Project section records the exact test command. |
| `GET /health` returns HTTP 200. | Started Uvicorn locally and called `/health` with curl on 2026-09-02. | PASS: HTTP 200 with `status: ok`. | Kept the health command in README and Docker evidence. |
| Tests do not use the real seed-data file. | `tests/conftest.py` plus existing `docs/midcourse/verification.md`. | PASS: tests use `TASKS_FILE` pointing to `tests/data/test_tasks.json`. | AGENTS.md preserves this as a project guardrail. |
| CI runs pytest without failure-hiding shortcuts. | `.github/workflows/ci.yml` manual inspection. | PASS: GitHub Actions ran successfully on `final-project`; 45 tests passed. | Added explicit dependency install and pytest step. |
| Docker image runs `/health` successfully. | Docker image built and container run in GitHub Codespaces on 2026-09-03; /health checked with curl. | PASS: HTTP/1.1 200 OK with status: ok. | Recorded successful Docker runtime verification from GitHub Codespaces. |
