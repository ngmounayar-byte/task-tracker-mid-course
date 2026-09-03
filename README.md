# Task Tracker API

A Task Tracker REST API built with Python and FastAPI, with a small static Kanban frontend.

This project started as the Module 1 skeleton and has since grown through Modules 1-3 and the mid-course project into a working task board with full CRUD, status-transition rules, due dates with an overdue filter, and tags/labels. See `docs/midcourse/` for the mid-course project's user stories, design decisions, prompt log, and verification evidence.

## Current scope

- A FastAPI application with full task CRUD (`POST`/`GET`/`PATCH`/`DELETE /tasks`)
- Status-transition validation (`app/business_rules.py`)
- Due dates with a live-computed, never-stored `is_overdue` flag, and an `overdue` query filter
- Validated tags (trimmed, deduplicated, capped count/length), with a case-insensitive `tag` query filter
- A JSON-file task repository (`app/data/tasks.json`)
- A static Kanban frontend (`frontend/index.html`) — drag-and-drop columns, an edit/create modal, overdue pills, tag chips, and a filter bar
- Interactive Swagger API documentation

## Architecture

The application will use the following layers:

```text
API routes
    ↓
Task service
    ↓
JSON task repository
    ↓
app/data/tasks.json
```

API routes must not access the JSON file directly. Future task operations will go through the service and repository layers.

## Requirements

- Python 3.10 or newer
- `pip`

Check your Python installation:

```bash
python --version
```

On Linux or macOS, you may need to use:

```bash
python3 --version
```

## Setup on Linux or macOS

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Create the local environment file:

```bash
cp .env.example .env
```

## Setup on Windows PowerShell

Create a virtual environment:

```powershell
py -m venv venv
```

Allow script execution for the current PowerShell process:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

Create the local environment file:

```powershell
Copy-Item .env.example .env
```

## Run the development server

Run this command from the project root:

```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The API will be available at:

```text
http://127.0.0.1:8000
```

The `--reload` option automatically restarts the development server when Python files change. It is intended for local development only.

## Open the frontend

With the server running, open:

```text
http://localhost:8000/
```

Use `localhost`, not `127.0.0.1` — the frontend's JavaScript makes API calls to `http://localhost:8000`, and the backend's CORS configuration does not allow the `127.0.0.1:8000` origin, so loading the page via `127.0.0.1` will cause every API request to fail silently.

The board loads tasks from the API, supports drag-and-drop between columns, and has a filter bar (overdue-only toggle, tag search) above the board. Click **Edit** on any card to open a modal covering all task fields, or **+ New Task** to create one.

## Run the tests

From the project root, with the virtual environment activated:

```bash
python -m pip install pytest httpx
python -m pytest tests/ -v
```

The test suite uses its own JSON data file (`tests/data/test_tasks.json`, created automatically and gitignored) so running tests never touches your real `app/data/tasks.json` seed data. This is controlled by the `TASKS_FILE` environment variable, set automatically in `tests/conftest.py`.

## Test the health endpoint

Using Bash:

```bash
curl http://127.0.0.1:8000/health
```

Using Windows PowerShell:

```powershell
curl.exe http://127.0.0.1:8000/health
```

Expected response shape:

```json
{
  "status": "ok",
  "timestamp": "2026-07-20T06:30:00.000000Z"
}
```

The timestamp value will be different for every request.

## Swagger documentation

Open the following URL in a browser:

```text
http://127.0.0.1:8000/docs
```

Swagger UI allows you to inspect and test the API endpoints interactively.

Alternative ReDoc documentation is available at:

```text
http://127.0.0.1:8000/redoc
```

## Stop the server

Press:

```text
Ctrl+C
```

## Installed dependency versions

The initial `requirements.txt` does not pin dependency versions.

After installing the dependencies, you can record the exact installed versions with:

```bash
python -m pip freeze > requirements.lock.txt
```
## Final Project

Branch reviewed: `final-project`

### What this submission demonstrates

- The existing Task Tracker stays within the intended course scope and its full pytest suite remains green.
- CI is configured to run pytest on push and pull request.
- A Docker image definition and Docker ignore rules are provided for repeatable runtime packaging.
- AI review, security review, release evidence, and ownership rules are documented under `docs/`.

### How to run locally

```bash
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open the frontend at `http://localhost:8000/` and check the Kanban board/create-edit flow.

### How to run tests

```bash
python -m pip install pytest httpx
python -m pytest tests/ -q
```

Final packaging check on 2026-09-02: `36 passed in 0.22s`.

### How to run with Docker

```bash
docker build -t task-tracker .
docker run --rm -p 8000:8000 task-tracker
curl -i http://127.0.0.1:8000/health
```

The Dockerfile runs the application as a non-root user. Record the real Docker build/run and `/health` result in `docs/release-evidence.md` before final submission.

### Evidence files

- `docs/release-evidence.md`
- `docs/final-ai-review.md`
- `docs/ai-playbook.md`
- `AGENTS.md`

### AI assistance summary

AI helped draft/review CI, Docker configuration, release documentation, and security/ownership evidence. The work was checked against the existing repository and the course requirements rather than accepting generated output blindly. Verification included a full pytest run, a local `/health` request, manual repository inspection, and review of earlier mid-course evidence. One earlier AI-generated tags behavior was corrected after tracing a `tags: null` edge case instead of accepting it as-is.
