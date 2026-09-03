# Release Evidence

## Baseline
- Branch required for final submission: `final-project`.
- Date checked: 2026-09-02.
- Local app run command: `python -m uvicorn app.main:app --host 127.0.0.1 --port 8765`.
- `/health` result: HTTP `200 OK` with JSON `{"status":"ok", ...}` on 2026-09-02.
- Frontend check: the repository serves `frontend/index.html` from `/`; the existing mid-course verification records a manual Kanban/create-edit browser check. A fresh browser check should be repeated by the submitter after cloning/pushing the final branch.
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
- Run command: `docker run --rm -p 8000:8000 task-tracker`.
- Container health command: `curl -i http://127.0.0.1:8000/health`.
- Expected result from application contract: HTTP `200` and a JSON body with `status: "ok"` and a timestamp.
- Non-root check: the Dockerfile creates `appuser` and switches to `USER appuser` before runtime.
- No-baked-secrets check: `.dockerignore` excludes `.env` and `.env.*`; only the application and frontend are copied after dependency installation.
- Local Docker verification: **NOT COMPLETED on this machine**.
- Reason: Docker Desktop was installed, but it could not start because virtualization support was not available on the current computer.
- Therefore, the Docker image build/run and container `/health` HTTP 200 check could not be verified locally.
- No successful Docker runtime result is claimed.

## Documentation claim-vs-reality log

| Claim checked | Evidence used | Result | Change made, if any |
|---|---|---|---|
| The full test suite passes. | `python -m pytest tests/ -q` | PASS: 45 passed, 4 warnings in 0.26s | README Final Project section records the exact test command. |
| `GET /health` returns HTTP 200. | Started Uvicorn locally and called `/health` with curl on 2026-09-02. | PASS: HTTP 200 with `status: ok`. | Kept the health command in README and Docker evidence. |
| Tests do not use the real seed-data file. | `tests/conftest.py` plus existing `docs/midcourse/verification.md`. | PASS: tests use `TASKS_FILE` pointing to `tests/data/test_tasks.json`. | AGENTS.md preserves this as a project guardrail. |
| CI runs pytest without failure-hiding shortcuts. | `.github/workflows/ci.yml` manual inspection. | PASS: GitHub Actions ran successfully on `final-project`; 45 tests passed. | Added explicit dependency install and pytest step. |
| Docker image runs `/health` successfully. | Dockerfile/config inspection only. | NOT YET RUNTIME-VERIFIED. | Left an explicit completion note instead of inventing a pass. |
