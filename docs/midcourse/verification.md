# Verification

## Baseline check

The original Modules 1–3 repository was not available in this submission. This limitation is stated transparently; the current repository cannot independently demonstrate preservation of that earlier baseline.

Baseline before feature work:
- FastAPI application started successfully.
- `GET /tasks` returned the initial task collection.
- Frontend loaded the three Kanban columns.
- Initial test suite status: no tests existed.

## Backend test results

Command:

```bash
pytest -q
```

Expected result:

```text
8 passed
```

Tests cover:
- Valid due date and tags
- Invalid date format
- Overdue filtering
- Completed task excluded from overdue
- Blank tag rejection
- Case-insensitive tag filtering
- Tag preservation after unrelated update
- Due-date update

## Manual browser checks

1. Opened `http://127.0.0.1:8000`.
2. Created a task with a due date and two tags.
3. Confirmed the due date and tag chips appeared on the card.
4. Edited the task and changed only its priority.
5. Confirmed tags and due date were preserved.
6. Filtered by tag using different letter casing.
7. Created a task with a past date and confirmed the overdue badge appeared.
8. Marked the overdue task as done and confirmed the overdue badge disappeared.
9. Applied the overdue filter and confirmed empty Kanban columns remained visible.

## Behavior contract used for focused refactor verification

- `POST /tasks` creates a task.
- `PATCH /tasks/{id}` updates only supplied fields.
- `DELETE /tasks/{id}` removes a task.
- `GET /tasks` returns tasks sorted by ID.
- Missing tasks return 404.

## Behavior contract after refactor

All baseline behavior remained unchanged, with these additions:
- Optional `due_date`
- Computed `overdue`
- Optional `overdue` query filter
- Validated `tags`
- Optional case-insensitive `tag` query filter

## Break Test evidence

### Break Test 1: completed tasks and overdue logic

Important test:

```text
test_done_task_is_not_overdue
```

Break introduced:
- Temporarily removed `task.status != Status.done` from the overdue property.

Observed result:
- The test failed because the completed past-due task appeared in the overdue result.

Fix:
- Restored the status exclusion.

### Break Test 2: preserving tags on partial update

Important test:

```text
test_unrelated_update_preserves_tags
```

Break introduced:
- Temporarily built PATCH data from the full update model instead of using `exclude_unset=True`.

Observed result:
- The test failed because omitted tags were replaced.

Fix:
- Restored `payload.model_dump(exclude_unset=True)`.


## Reviewer corrections

- Explicit `null` values for `title`, `status`, `priority`, and `tags` now return HTTP 422.
- Frontend task loading, deletion, save, and network failures now display visible error messages.
- Feature behavior and behavior-preserving refactoring are documented separately.

## Baseline limitation

Because the original Modules 1–3 repository and its Git history were not available, this submission does not claim that the earlier baseline has been proven. A complete resubmission would require importing the genuine earlier project and its existing tests before the mid-course changes.
