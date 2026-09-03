# Release Evidence

## Baseline
- Branch required for final submission: `final-project`.
- Date checked: 2026-09-02.
- Local app run command: `python -m uvicorn app.main:app --host 127.0.0.1 --port 8765`.
- `/health` result: HTTP `200 OK` with JSON `{"status":"ok", ...}` on 2026-09-02.
- Frontend check: the repository serves `frontend/index.html` from `/`; the existing mid-course verification records a manual Kanban/create-edit browser check. A fresh browser check should be repeated by the submitter after cloning/pushing the final branch.
- Test command: `python -m pytest tests/ -q`.
- Test result: `36 passed in 0.22s` on 2026-09-02.

## CI evidence
- Workflow file: `.github/workflows/ci.yml`.
- Trigger: push and pull request.
- Python version: `3.11`.
- Dependency installation: installs `requirements.txt`, then `pytest` and `httpx` required by the test suite.
- Test command used by CI: `python -m pytest tests/ -q`.
- Shortcut check: no `continue-on-error`, no `|| true`, pytest is not skipped, and dependency installation is explicit.
- Latest GitHub Actions run link or note: **TO COMPLETE AFTER PUSHING `final-project` TO GITHUB.** Replace this sentence with the green Actions run URL or an honest run-status note.

## Docker evidence
- Dockerfile: `Dockerfile`.
- Ignore file: `.dockerignore`.
- Build command: `docker build -t task-tracker .`.
- Run command: `docker run --rm -p 8000:8000 task-tracker`.
- Container health command: `curl -i http://127.0.0.1:8000/health`.
- Expected result from application contract: HTTP `200` and a JSON body with `status: "ok"` and a timestamp.
- Non-root check: the Dockerfile creates `appuser` and switches to `USER appuser` before runtime.
- No-baked-secrets check: `.dockerignore` excludes `.env` and `.env.*`; only the application and frontend are copied after dependency installation.
- Runtime verification: **TO COMPLETE ON A MACHINE WITH DOCKER.** Docker is not available in the review environment used to assemble this package, so no Docker build/run result is claimed here. Run the three commands above and replace this note with the real result before submission.

## Documentation claim-vs-reality log

| Claim checked | Evidence used | Result | Change made, if any |
|---|---|---|---|
| The full test suite passes. | `python -m pytest tests/ -q` | PASS: 36 passed in 0.22s | README Final Project section records the exact test command. |
| `GET /health` returns HTTP 200. | Started Uvicorn locally and called `/health` with curl on 2026-09-02. | PASS: HTTP 200 with `status: ok`. | Kept the health command in README and Docker evidence. |
| Tests do not use the real seed-data file. | `tests/conftest.py` plus existing `docs/midcourse/verification.md`. | PASS: tests use `TASKS_FILE` pointing to `tests/data/test_tasks.json`. | AGENTS.md preserves this as a project guardrail. |
| CI runs pytest without failure-hiding shortcuts. | `.github/workflows/ci.yml` manual inspection. | PASS by configuration; GitHub-hosted execution still needs to be recorded. | Added explicit dependency install and pytest step. |
| Docker image runs `/health` successfully. | Dockerfile/config inspection only. | NOT YET RUNTIME-VERIFIED. | Left an explicit completion note instead of inventing a pass. |
