# Prompt Log

## Feature 1: Due dates and overdue filter

### Prompt 1 — weak
> Add due dates.

**Why it was weak**
It did not define validation, overdue behavior, update behavior, or tests.

### Prompt 1 — rewritten
> Extend the FastAPI Task model with an optional ISO due date. Support create and PATCH update. Return a computed overdue boolean that is true only when the due date is before today and status is not done. Add an optional overdue query filter. Keep storage in memory and provide focused pytest tests.

**AI response summary**
AI proposed model fields, a computed overdue rule, endpoint changes, and tests.

**Decision**
Accepted the general structure. Edited the rule to explicitly exclude completed tasks.

### Prompt 2
> Add a date input to the task modal, show a due-date badge on cards, and add an overdue filter above the board. Keep all Kanban columns visible even when filtered.

**AI response summary**
AI proposed modal markup, fetch query parameters, and card rendering.

**Decision**
Accepted with minor naming edits.

### Prompt 3
> Review the due-date implementation for edge cases and list the minimum tests needed.

**AI response summary**
AI identified invalid dates, completed past-due tasks, updates, and filtering.

**Decision**
Accepted and added these cases to pytest.

## Feature 2: Tags and tag filtering

### Prompt 1
> Add tags to each task as a list of strings. Trim values, reject blanks, cap tags at eight, remove case-insensitive duplicates, support PATCH updates, and preserve tags during unrelated updates.

**AI response summary**
AI proposed Pydantic validators and partial-update logic.

**Decision**
Accepted. Rejected a normalized database design because the app has no database.

### Prompt 2
> Add comma-separated tags to the modal, render each as a chip, and add a case-insensitive tag filter above the board.

**AI response summary**
AI proposed input parsing, chip rendering, and query-string filtering.

**Decision**
Accepted with HTML escaping added during review.

### Prompt 3
> Write pytest tests for blank-tag rejection, case-insensitive filtering, and preservation after an unrelated PATCH.

**AI response summary**
AI generated focused endpoint tests.

**Decision**
Accepted after ensuring the test store resets between tests.
