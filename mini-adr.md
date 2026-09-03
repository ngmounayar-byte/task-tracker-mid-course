# Mini ADR: Due Dates + Overdue Filter, and Tags/Labels

## Context

The Task Tracker (FastAPI + JSON-file repository + vanilla-JS Kanban frontend) needed two scoped features added for the mid-course project: **due dates with an overdue filter**, and **tags/labels**. This note records the decisions made, the alternatives considered, and what was rejected as out of scope.

## Decision 1: `due_date` as a native `date` field, not a string

**Chosen:** `due_date: Optional[date]` on `TaskCreate`/`TaskUpdate`/`TaskResponse`.

**Alternative considered:** store it as a plain string and validate format with a custom `field_validator` (mirroring how `title` is validated).

**Rejected because:** Pydantic's `date` type already performs ISO-8601 validation for free — a malformed value like `"not-a-date"` is rejected with `422` with zero custom code. Writing a custom string validator would just be reimplementing what the type system already gives us, for no benefit.

## Decision 2: `is_overdue` computed live at read time, never stored

**Chosen:** a business-rule function `is_overdue(due_date, status)` in `app/business_rules.py`, applied by the repository every time a task is constructed or read from disk. The field is explicitly excluded from what gets persisted to `tasks.json`.

**Alternatives considered:**
- Store `is_overdue` as a flag set once at create/update time.
- Compute it only in the frontend, treating the API as unaware of "overdue" entirely.

**Rejected because:**
- Storing it would go stale — a task doesn't change when it *becomes* overdue merely because a day passed; nothing writes to it on that day. A stored flag would only be correct until midnight after the last edit.
- Computing it only in the frontend would make the `overdue` query filter impossible to implement server-side (the brief explicitly asks for an optional query filter), and would duplicate the "what counts as overdue" business rule in two places (JS and Python) instead of one.

**Trade-off accepted:** every read does a small amount of extra computation (checking today's date). This is negligible for a JSON-file-backed hobby-scale tracker and is the correct choice for correctness over the alternative's cost savings.

**Implementation detail worth recording:** `is_overdue` is a plain Pydantic field, not a `@computed_field`. A `computed_field` would conflict with `model_config = ConfigDict(extra="forbid")` on round-trips through the JSON file (the stored dict would carry a key that isn't a normal settable input). A plain field, explicitly excluded from `model_dump()` at write time and explicitly re-applied at read time via a small `_with_computed()` helper in the repository, avoids that conflict entirely.

## Decision 3: overdue excludes `Done` tasks

**Chosen:** `is_overdue` is `true` only if `due_date < today` **and** `status != Done`.

**Alternative considered:** any task with a past due date is overdue, regardless of status.

**Rejected because:** a task marked `Done` isn't something that needs attention — flagging it as "overdue" would just be noise on the board. This was decided during design, before writing the implementation, and is directly covered by a test (`test_task_with_past_due_date_but_done_status_is_not_overdue`) and a documented Break Test (see `docs/verification.md`) proving the exclusion actually matters.

## Decision 4: `tags` as `list[str]`, not a comma-separated string

**Chosen:** `tags: list[str]` on the model, normalized (trimmed, deduplicated) and validated (reject blank, cap count and length) by a `field_validator`.

**Alternative considered:** store tags as a single comma-separated string field (as the brief's feature table explicitly allows: "a list or normalized comma-separated field").

**Rejected because:** a comma-separated string pushes escaping problems onto every caller (what if a tag itself contains a comma?), makes the case-insensitive `?tag=` filter harder to implement correctly, and makes the OpenAPI schema less useful (Swagger shows a real array instead of an opaque string). A `list[str]` is the more honest representation of "a task has zero or more tags" and costs nothing extra given JSON already supports arrays natively.

## Decision 5: tag validation caps (10 tags, 30 chars) are explicit constants, not configurable

**Chosen:** `MAX_TAGS = 10` and `MAX_TAG_LENGTH = 30` as module-level constants in `app/models/task.py`.

**Rejected as out of scope:** making these configurable via environment variables or a settings object. The brief calls for an "optional maximum count/length," not a configurable one — adding configurability here would be speculative complexity for a limit nobody has asked to change.

## Decision 6: Edit-only modal, no "create task" flow (later revised)

**Original decision:** the frontend had no working task-creation UI before this work (the "Edit" button was a stub `alert()`), and neither due dates nor tags requires a creation flow to satisfy the brief. The initial choice was to build a real **edit** modal only, covering all fields including the two new ones, and leave creation to the API/Swagger UI — keeping frontend scope tied strictly to what the two features need.

**Revised:** the user asked for a "New Task" button after seeing the working edit modal. This was added by reusing the same modal in a `create` mode (different title/button text, `POST` instead of `PATCH`, empty/default field values) rather than building a second form — the marginal cost was small once the modal, validation display, and refetch logic already existed.

**Rejected alternative:** a separate creation form/page. Not justified — the edit modal already has every field a creation flow needs.

## Decision 7: fix test/dev data isolation before adding more tests

**Chosen:** make the JSON repository's file path configurable via a `TASKS_FILE` environment variable; point `tests/conftest.py` at a separate, gitignored file (`tests/data/test_tasks.json`).

**Why it's in scope:** this isn't feature work, but `tests/conftest.py` and `app/main.py` shared the exact same physical file (`app/data/tasks.json`) before this change — running pytest reset the real seed data to empty every time (verified: it happened once during this session, restored via `git checkout`). Adding ~18 new tests across two features without fixing this would have meant repeatedly destroying dev data during normal development. A one-line env-var change removes the risk entirely.

**Rejected as overkill:** switching the whole app off JSON-file storage onto SQLite/Postgres for "proper" test isolation. Out of scope — the brief doesn't ask for a storage-layer change, and the existing JSON repository pattern works fine once test and dev data are pointed at different files.
