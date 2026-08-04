from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient

import app as task_app


@pytest.fixture(autouse=True)
def reset_store():
    task_app.tasks.clear()
    task_app.next_id = 1
    yield
    task_app.tasks.clear()


@pytest.fixture
def client():
    return TestClient(task_app.app)


def make_task(client, **overrides):
    payload = {
        "title": "Example task",
        "description": "A test task",
        "status": "todo",
        "priority": "medium",
        "assignee": "Nathalie",
        "due_date": None,
        "tags": [],
    }
    payload.update(overrides)
    return client.post("/tasks", json=payload)


def test_create_task_with_due_date_and_tags(client):
    response = make_task(
        client,
        due_date=(date.today() + timedelta(days=2)).isoformat(),
        tags=["frontend", "urgent"],
    )

    assert response.status_code == 201
    body = response.json()
    assert body["due_date"] == (date.today() + timedelta(days=2)).isoformat()
    assert body["tags"] == ["frontend", "urgent"]
    assert body["overdue"] is False


def test_invalid_due_date_returns_422(client):
    response = make_task(client, due_date="not-a-date")

    assert response.status_code == 422


def test_overdue_filter_returns_only_overdue_tasks(client):
    overdue_date = (date.today() - timedelta(days=1)).isoformat()
    future_date = (date.today() + timedelta(days=1)).isoformat()

    make_task(client, title="Late task", due_date=overdue_date)
    make_task(client, title="Future task", due_date=future_date)

    response = client.get("/tasks", params={"overdue": "true"})

    assert response.status_code == 200
    assert [task["title"] for task in response.json()] == ["Late task"]


def test_done_task_is_not_overdue(client):
    overdue_date = (date.today() - timedelta(days=1)).isoformat()
    make_task(client, title="Completed late task", due_date=overdue_date, status="done")

    response = client.get("/tasks", params={"overdue": "true"})

    assert response.status_code == 200
    assert response.json() == []


def test_blank_tag_is_rejected(client):
    response = make_task(client, tags=["frontend", "   "])

    assert response.status_code == 422


def test_filter_by_tag_is_case_insensitive(client):
    make_task(client, title="UI task", tags=["FrontEnd"])
    make_task(client, title="API task", tags=["backend"])

    response = client.get("/tasks", params={"tag": "frontend"})

    assert response.status_code == 200
    assert [task["title"] for task in response.json()] == ["UI task"]


def test_unrelated_update_preserves_tags(client):
    created = make_task(client, tags=["frontend", "urgent"]).json()

    response = client.patch(
        f"/tasks/{created['id']}",
        json={"priority": "high"},
    )

    assert response.status_code == 200
    assert response.json()["tags"] == ["frontend", "urgent"]
    assert response.json()["priority"] == "high"


def test_update_due_date(client):
    created = make_task(client).json()
    new_date = (date.today() + timedelta(days=7)).isoformat()

    response = client.patch(
        f"/tasks/{created['id']}",
        json={"due_date": new_date},
    )

    assert response.status_code == 200
    assert response.json()["due_date"] == new_date


@pytest.mark.parametrize("field_name", ["title", "status", "priority", "tags"])
def test_create_rejects_explicit_null_required_fields(client, field_name):
    payload = {
        "title": "Example task",
        "description": "A test task",
        "status": "todo",
        "priority": "medium",
        "assignee": "Nathalie",
        "due_date": None,
        "tags": [],
    }
    payload[field_name] = None
    response = client.post("/tasks", json=payload)
    assert response.status_code == 422


@pytest.mark.parametrize("field_name", ["title", "status", "priority", "tags"])
def test_update_rejects_explicit_null_required_fields(client, field_name):
    created = make_task(client).json()
    response = client.patch(f"/tasks/{created['id']}", json={field_name: None})
    assert response.status_code == 422


def test_update_allows_omitted_fields(client):
    created = make_task(client, tags=["frontend"]).json()
    response = client.patch(
        f"/tasks/{created['id']}",
        json={"description": "Updated description"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == created["title"]
    assert response.json()["tags"] == ["frontend"]
