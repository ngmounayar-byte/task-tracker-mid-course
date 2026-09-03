from __future__ import annotations

from enum import Enum
from typing import Optional
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, field_validator


class TaskStatus(str, Enum):
    TODO = "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"


class TaskPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


MAX_TAGS = 10
MAX_TAG_LENGTH = 30


def _validate_tags(v):
    if v is None:
        return v
    if not isinstance(v, list):
        raise TypeError("tags must be a list of strings")
    if len(v) > MAX_TAGS:
        raise ValueError(f"a task may not have more than {MAX_TAGS} tags")

    cleaned: list[str] = []
    for tag in v:
        if not isinstance(tag, str):
            raise TypeError("each tag must be a string")
        tag = tag.strip()
        if not tag:
            raise ValueError("tags must not be blank")
        if len(tag) > MAX_TAG_LENGTH:
            raise ValueError(f"a tag must not exceed {MAX_TAG_LENGTH} characters")
        if tag not in cleaned:
            cleaned.append(tag)
    return cleaned


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str
    description: Optional[str] = ""
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: Optional[str] = None
    due_date: Optional[date] = None
    tags: list[str] = []

    @field_validator("title", mode="before")
    def _strip_and_validate_title(cls, v):
        if not isinstance(v, str):
            raise TypeError("title must be a string")
        v = v.strip()
        if not v:
            raise ValueError("title must not be blank")
        if len(v) > 200:
            raise ValueError("title must not exceed 200 characters")
        return v

    @field_validator("tags", mode="before")
    def _validate_tags(cls, v):
        return _validate_tags(v) if v is not None else []


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee: Optional[str] = None
    due_date: Optional[date] = None
    tags: Optional[list[str]] = None

    @field_validator("title", mode="before")
    def _strip_and_validate_title(cls, v):
        if v is None:
            return v
        if not isinstance(v, str):
            raise TypeError("title must be a string")
        v = v.strip()
        if not v:
            raise ValueError("title must not be blank")
        if len(v) > 200:
            raise ValueError("title must not exceed 200 characters")
        return v

    @field_validator("tags", mode="before")
    def _validate_tags(cls, v):
        # An explicit `null` clears the tag list rather than being stored as
        # None, since TaskResponse.tags is a plain (non-Optional) list.
        if v is None:
            return []
        return _validate_tags(v)


class TaskResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    assignee: Optional[str]
    due_date: Optional[date] = None
    is_overdue: bool = False
    tags: list[str] = []
    created_at: datetime
    updated_at: datetime
