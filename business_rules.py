from datetime import date, datetime, timezone
from typing import Optional

from fastapi import HTTPException, status

from app.models import TaskStatus

VALID_TRANSITIONS: frozenset[tuple[TaskStatus, TaskStatus]] = frozenset({
    (TaskStatus.TODO, TaskStatus.IN_PROGRESS),
    (TaskStatus.IN_PROGRESS, TaskStatus.DONE),
    (TaskStatus.DONE, TaskStatus.IN_PROGRESS),
    (TaskStatus.TODO, TaskStatus.TODO), # Allow same status transition for idempotency
    (TaskStatus.IN_PROGRESS, TaskStatus.IN_PROGRESS), # Allow same status transition for idempotency
    (TaskStatus.DONE, TaskStatus.DONE), # Allow same status transition for idempotency
})


def validate_status_transition(current: TaskStatus, new: TaskStatus) -> None:
    # Same -> same is invalid. Anything not in VALID_TRANSITIONS is invalid.
    if (current, new) not in VALID_TRANSITIONS:
        allowed = sorted({f"{f.value}->{t.value}" for f, t in VALID_TRANSITIONS})
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"Invalid status transition from {current.value} to {new.value}. Allowed transitions: {allowed}",
        )


def is_overdue(due_date: Optional[date], status: TaskStatus) -> bool:
    """A task is overdue if it has a due date in the past and is not Done."""
    if due_date is None:
        return False
    today = datetime.now(timezone.utc).date()
    return due_date < today and status != TaskStatus.DONE
