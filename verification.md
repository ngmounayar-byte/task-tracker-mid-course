# Verification

## 1. Baseline (before any changes)

Ran before touching any code, on branch `main`, after installing dependencies into a fresh venv:

```
$ python -m pytest tests/ -v
...
18 passed, 1 warning in 0.62s
```

All 18 pre-existing tests passed. The one warning (`StarletteDeprecationWarning` about `httpx`/`starlette.testclient`) is pre-existing and unrelated to this work — left as-is since fixing it is out of scope.

The frontend was also manually opened at `http://localhost:8000/` and confirmed to render the Kanban board (3 columns, drag-and-drop) correctly before any changes.

**Pre-existing issue found and fixed as prerequisite work:** `tests/conftest.py` and `app/main.py` both pointed at the same physical file, `app/data/tasks.json`. Running the baseline pytest suite actually wiped the real seed data to `[]` (confirmed via `git diff app/data/tasks.json`, then restored via `git checkout -- app/data/tasks.json`). Fixed before adding any feature tests by making the repository path configurable via a `TASKS_FILE` environment variable, with `tests/conftest.py` pointing at a separate, gitignored `tests/data/test_tasks.json`. Re-ran the suite afterward and confirmed `app/data/tasks.json` was untouched (`git status --short` showed no change to that file).

## 2. Backend test results after both features

```
$ python -m pytest tests/ -v
...
tests/test_due_dates.py .......... (8 passed)
tests/test_tags.py .......... (10 passed)
tests/test_tasks.py .................. (18 passed)
======================== 36 passed, 1 warning in 0.70-0.77s ========================
```

36/36 passing: the original 18 unmodified, plus 8 new for due dates and 10 new for tags.

## 3. Manual browser checks

- Opened `http://localhost:8000/` (not `127.0.0.1` — the frontend's `fetch` calls are hardcoded to `http://localhost:8000`, and the backend's CORS allowlist doesn't include a `127.0.0.1:8000` origin, so loading via `127.0.0.1` would silently break every fetch call due to a cross-origin block).
- Created sample tasks via `curl` with a past due date and multiple tags to have real data to look at:
  - `"Ship the release notes"` — due `2026-07-20` (past, relative to the session date of 2026-07-28), status `ToDo`, tags `["docs", "urgent"]` → confirmed `is_overdue: true` in the API response and a red "Overdue" pill on the card in the browser.
  - `"Plan next sprint"` — due `2026-08-15` (future), tags `["planning"]` → confirmed no overdue pill, tag chip rendered correctly.
- Confirmed with the user directly (in-session) that: the overdue pill renders, tag chips render, and the Edit modal opens/pre-fills/saves correctly.
- After adding the "New Task" button (a scope addition requested mid-session), confirmed with the user that it opens the modal in create mode, submits via `POST`, and the new task appears on the board.

## 4. Behavior contract: before vs. after

| Endpoint | Before | After |
|---|---|---|
| `POST /tasks` | accepted `title, description, status, priority, assignee` | additionally accepts optional `due_date`, `tags` — both optional, fully backward compatible with old request bodies |
| `PATCH /tasks/{id}` | same fields as above, partial update | additionally accepts `due_date`, `tags` for partial update; omitting either leaves the existing value untouched (verified by `test_patch_unrelated_field_preserves_due_date` and `test_patch_unrelated_field_preserves_tags`) |
| `GET /tasks` | filters: `status`, `priority` | additionally: `overdue` (bool), `tag` (case-insensitive string match) — both optional, existing filters unaffected |
| Task response shape | `id, title, description, status, priority, assignee, created_at, updated_at` | additionally: `due_date` (nullable), `is_overdue` (bool, always present, computed live), `tags` (list, defaults to `[]`) |

No existing field, endpoint, or status-transition rule (`app/business_rules.py`'s `VALID_TRANSITIONS`) was changed. All 18 original tests pass unmodified against the new code, confirming backward compatibility.

No structural refactor was needed after implementation — the additions followed the existing layered pattern (route → service → repository → model) exactly, so there was nothing obviously duplicated to clean up. The only "refactor-shaped" change was the test-data isolation fix in section 1, which was done as prerequisite work before feature code, not as a post-hoc cleanup.

## 5. Break Test evidence

Per the brief, "run a Break Test for at least one important test" per feature — deliberately break the implementation, confirm the relevant test fails, then revert.

### Break Test 1 — Due dates (`is_overdue` excludes Done status)

**Break:** in `app/business_rules.py`, temporarily changed:
```python
return due_date < today and status != TaskStatus.DONE
```
to:
```python
return due_date < today  # Done-status exclusion removed
```

**Result — test failed as expected:**
```
tests/test_due_dates.py::test_task_with_past_due_date_but_done_status_is_not_overdue
    assert response.json()["is_overdue"] is False
E   assert True is False
FAILED tests/test_due_dates.py::test_task_with_past_due_date_but_done_status_is_not_overdue
1 failed, 1 passed in 0.18s
```

This confirms the test genuinely exercises the Done-status exclusion, rather than passing regardless of the implementation.

**Revert:** restored the original `and status != TaskStatus.DONE` condition. Full suite re-run: 36/36 passing again.

### Break Test 2 — Tags (blank-tag rejection)

**Break:** in `app/models/task.py`'s `_validate_tags()`, temporarily removed:
```python
if not tag:
    raise ValueError("tags must not be blank")
```

**Result — both tests failed as expected:**
```
tests/test_tags.py::test_create_task_with_blank_tag_returns_422
    assert response.status_code == 422
E   assert 201 == 422

tests/test_tags.py::test_update_tags_with_blank_tag_returns_422
    assert response.status_code == 422
E   assert 200 == 422

2 failed, 1 warning in 0.17s
```

This confirms both tests genuinely exercise the blank-tag rejection (one on create, one on update) rather than trivially passing.

**Revert:** restored the blank-tag check. Full suite re-run: 36/36 passing again.

## 6. Final state

```
$ python -m pytest tests/ -q
....................................
36 passed, 1 warning in 0.73s
```
