# Task Tracker — Mid-Course Project

A small full-stack Task Tracker built with FastAPI and vanilla JavaScript.

## Selected features

1. **Due dates and overdue filtering**
   - Optional due date on create and update
   - Date validation
   - Overdue badge on cards
   - Overdue-only and not-overdue filters

2. **Tags and tag filtering**
   - Up to 8 trimmed, non-empty tags
   - Case-insensitive duplicate removal
   - Tag chips on cards
   - Case-insensitive tag filter

## Branch

The submission branch is:

```text
mid-course-project
```

## Run the backend

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install and run:

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

## Open the frontend

Open this address in a browser:

```text
http://127.0.0.1:8000
```

## Run tests

```bash
pytest -q
```

## Project structure

```text
app.py
static/
  index.html
  app.js
  styles.css
tests/
  test_tasks.py
docs/
  midcourse/
    user-stories.md
    mini-adr.md
    prompt-log.md
    verification.md
    reflection.md
```

## Notes

- Data is stored in memory for simplicity and resets when the server restarts.
- No credentials, secrets, private data, or unrelated generated files are included.
