from datetime import date, timedelta


def test_create_task_with_valid_due_date_returns_201(client):
    due = (date.today() + timedelta(days=3)).isoformat()

    response = client.post("/tasks", json={"title": "Task with due date", "due_date": due})

    assert response.status_code == 201
    body = response.json()
    assert body["due_date"] == due
    assert body["is_overdue"] is False


def test_create_task_with_invalid_due_date_format_returns_422(client):
    response = client.post(
        "/tasks", json={"title": "Task with bad date", "due_date": "not-a-date"}
    )

    assert response.status_code == 422


def test_task_with_past_due_date_and_not_done_is_overdue(client):
    past = (date.today() - timedelta(days=1)).isoformat()

    response = client.post(
        "/tasks", json={"title": "Overdue task", "status": "ToDo", "due_date": past}
    )

    assert response.status_code == 201
    assert response.json()["is_overdue"] is True


def test_task_with_past_due_date_but_done_status_is_not_overdue(client):
    past = (date.today() - timedelta(days=1)).isoformat()

    response = client.post(
        "/tasks", json={"title": "Finished task", "status": "Done", "due_date": past}
    )

    assert response.status_code == 201
    assert response.json()["is_overdue"] is False


def test_update_due_date_changes_value(client, created_task):
    task_id = created_task["id"]
    new_due = (date.today() + timedelta(days=7)).isoformat()

    response = client.patch(f"/tasks/{task_id}", json={"due_date": new_due})

    assert response.status_code == 200
    assert response.json()["due_date"] == new_due


def test_patch_unrelated_field_preserves_due_date(client):
    due = (date.today() + timedelta(days=5)).isoformat()
    created = client.post("/tasks", json={"title": "Task", "due_date": due}).json()

    response = client.patch(f"/tasks/{created['id']}", json={"assignee": "bob"})

    assert response.status_code == 200
    assert response.json()["due_date"] == due


def test_list_tasks_filter_overdue_true_returns_only_overdue_tasks(client):
    past = (date.today() - timedelta(days=1)).isoformat()
    future = (date.today() + timedelta(days=1)).isoformat()
    client.post("/tasks", json={"title": "Overdue", "status": "ToDo", "due_date": past})
    client.post("/tasks", json={"title": "Not overdue", "status": "ToDo", "due_date": future})
    client.post("/tasks", json={"title": "No due date"})

    response = client.get("/tasks", params={"overdue": "true"})

    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Overdue"


def test_list_tasks_filter_overdue_false_excludes_overdue_tasks(client):
    past = (date.today() - timedelta(days=1)).isoformat()
    future = (date.today() + timedelta(days=1)).isoformat()
    client.post("/tasks", json={"title": "Overdue", "status": "ToDo", "due_date": past})
    client.post("/tasks", json={"title": "Not overdue", "status": "ToDo", "due_date": future})

    response = client.get("/tasks", params={"overdue": "false"})

    assert response.status_code == 200
    titles = [t["title"] for t in response.json()]
    assert titles == ["Not overdue"]
