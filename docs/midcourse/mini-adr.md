# Mini ADR

## Decision

Implement two features:

1. Due dates with overdue computation and filtering.
2. Tags with tag filtering.

The backend is FastAPI with an in-memory task store. The frontend is a responsive vanilla JavaScript Kanban board.

## Due-date design

The backend computes the `overdue` value because this keeps the rule consistent for every client. A task is overdue only when:

- it has a due date,
- the due date is before today, and
- its status is not `done`.

### Alternatives considered

- **Compute overdue only in JavaScript:** rejected because API clients could disagree.
- **Persist an overdue boolean:** rejected because it can become stale.
- **Add database indexing:** rejected because persistence was outside this scoped project.

## Tag design

Tags are stored as a validated list of strings on each task.

### Alternatives considered

- **Normalized tag and task-tag database tables:** rejected as too complex for an in-memory app.
- **Single comma-separated database field:** rejected because list validation and filtering are clearer with structured data.
- **Free-text tags with no limits:** rejected to prevent blank values and uncontrolled input.

## Scope controls

- No authentication.
- No database.
- No drag-and-drop.
- No bulk operations.
- No saved views.
- No frontend framework.

These exclusions keep both selected features small, testable, and explainable.
