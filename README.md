from __future__ import annotations

from datetime import date
from enum import Enum
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="Task Tracker", version="1.0.0")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


class Status(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    description: str = Field(default="", max_length=1000)
    status: Status = Status.todo
    priority: Priority = Priority.medium
    assignee: str = Field(default="", max_length=80)
    due_date: Optional[date] = None
    tags: list[str] = Field(default_factory=list, max_length=8)

    @field_validator("title", "assignee")
    @classmethod
    def strip_text(cls, value: str) -> str:
        return value.strip()

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, value: str) -> str:
        if not value:
            raise ValueError("Title must not be blank")
        return value

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, tags: list[str]) -> list[str]:
        normalized: list[str] = []
        for raw_tag in tags:
            tag = raw_tag.strip()
            if not tag:
                raise ValueError("Tags must not be blank")
            if len(tag) > 30:
                raise ValueError("Each tag must be 30 characters or fewer")
            if tag.lower() not in [existing.lower() for existing in normalized]:
                normalized.append(tag)
        return normalized


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=120)
    description: Optional[str] = Field(default=None, max_length=1000)
    status: Optional[Status] = None
    priority: Optional[Priority] = None
    assignee: Optional[str] = Field(default=None, max_length=80)
    due_date: Optional[date] = None
    tags: Optional[list[str]] = Field(default=None, max_length=8)

    @field_validator("title", "assignee")
    @classmethod
    def strip_optional_text(cls, value: Optional[str]) -> Optional[str]:
        return value.strip() if value is not None else None

    @field_validator("title")
    @classmethod
    def optional_title_must_not_be_blank(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and not value:
            raise ValueError("Title must not be blank")
        return value

    @field_validator("tags")
    @classmethod
    def validate_optional_tags(cls, tags: Optional[list[str]]) -> Optional[list[str]]:
        if tags is None:
            return None
        normalized: list[str] = []
        for raw_tag in tags:
            tag = raw_tag.strip()
            if not tag:
                raise ValueError("Tags must not be blank")
            if len(tag) > 30:
                raise ValueError("Each tag must be 30 characters or fewer")
            if tag.lower() not in [existing.lower() for existing in normalized]:
                normalized.append(tag)
        return normalized


class Task(TaskBase):
    id: int

    @property
    def overdue(self) -> bool:
        return self.due_date is not None and self.due_date < date.today() and self.status != Status.done


tasks: dict[int, Task] = {}
next_id = 1


def seed_tasks() -> None:
    global next_id
    if tasks:
        return
    sample_tasks = [
        Task(
            id=1,
            title="Prepare project brief",
            description="Review scope and acceptance criteria.",
            status=Status.todo,
            priority=Priority.high,
            assignee="Nathalie",
            due_date=None,
            tags=["planning"],
        ),
        Task(
            id=2,
            title="Build Kanban UI",
            description="Create responsive columns and task cards.",
            status=Status.in_progress,
            priority=Priority.medium,
            assignee="Nathalie",
            due_date=None,
            tags=["frontend", "ui"],
        ),
        Task(
            id=3,
            title="Add API tests",
            description="Cover create, update, overdue, and tag filtering.",
            status=Status.done,
            priority=Priority.high,
            assignee="Nathalie",
            due_date=None,
            tags=["testing"],
        ),
    ]
    tasks.update({task.id: task for task in sample_tasks})
    next_id = 4


seed_tasks()


@app.get("/")
def home() -> FileResponse:
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.get("/tasks")
def list_tasks(
    overdue: Optional[bool] = Query(default=None),
    tag: Optional[str] = Query(default=None),
) -> list[dict]:
    result = list(tasks.values())

    if overdue is not None:
        result = [task for task in result if task.overdue is overdue]

    if tag:
        wanted = tag.strip().lower()
        result = [
            task for task in result
            if any(existing.lower() == wanted for existing in task.tags)
        ]

    return [
        {
            **task.model_dump(mode="json"),
            "overdue": task.overdue,
        }
        for task in sorted(result, key=lambda item: item.id)
    ]


@app.post("/tasks", status_code=201)
def create_task(payload: TaskCreate) -> dict:
    global next_id
    task = Task(id=next_id, **payload.model_dump())
    tasks[next_id] = task
    next_id += 1
    return {**task.model_dump(mode="json"), "overdue": task.overdue}


@app.patch("/tasks/{task_id}")
def update_task(task_id: int, payload: TaskUpdate) -> dict:
    current = tasks.get(task_id)
    if current is None:
        raise HTTPException(status_code=404, detail="Task not found")

    changes = payload.model_dump(exclude_unset=True)
    updated = current.model_copy(update=changes)
    tasks[task_id] = updated
    return {**updated.model_dump(mode="json"), "overdue": updated.overdue}


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int) -> None:
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    del tasks[task_id]
