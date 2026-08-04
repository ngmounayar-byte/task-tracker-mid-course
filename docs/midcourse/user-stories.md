# User Stories

## Feature 1: Due dates and overdue filtering

### Story 1
As a user, I want to assign an optional due date to a task so that I know when it should be completed.

**Acceptance criteria**
- The create and edit forms accept a valid ISO date.
- The due date is optional.
- An invalid date returns HTTP 422.

### Story 2
As a user, I want overdue tasks to be visibly marked so that I can prioritize them.

**Acceptance criteria**
- A task is overdue when its due date is before today.
- Completed tasks are never marked overdue.
- Overdue tasks display an overdue badge in the frontend.

### Story 3
As a user, I want to filter the board to overdue tasks so that I can focus on late work.

**Acceptance criteria**
- `GET /tasks?overdue=true` returns only overdue tasks.
- `GET /tasks?overdue=false` returns only tasks that are not overdue.
- Empty columns remain visible in the Kanban board.

**AI assumption corrected**
AI initially treated every task with a past due date as overdue. I corrected the rule so completed tasks are excluded.

## Feature 2: Tags and tag filtering

### Story 1
As a user, I want to add tags to tasks so that I can categorize work.

**Acceptance criteria**
- The modal accepts comma-separated tags.
- Tags are trimmed before storage.
- Blank tags are rejected.
- A maximum of eight tags is allowed.

### Story 2
As a user, I want tags displayed as chips on task cards so that categories are easy to scan.

**Acceptance criteria**
- Each tag appears as a separate chip.
- Tags remain visible after unrelated task updates.
- Duplicate tags are removed case-insensitively.

### Story 3
As a user, I want to filter tasks by tag so that I can find related work quickly.

**Acceptance criteria**
- `GET /tasks?tag=frontend` returns tasks tagged `frontend`.
- Tag matching is case-insensitive.
- No matches return HTTP 200 with an empty list.

**AI assumption corrected**
AI first suggested a separate normalized tag table. I rejected that as unnecessary for an in-memory course project and used a validated list on each task.
