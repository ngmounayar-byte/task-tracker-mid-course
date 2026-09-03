def test_create_task_with_tags_returns_201_with_tags(client):
    response = client.post(
        "/tasks", json={"title": "Tagged task", "tags": ["backend", "urgent"]}
    )

    assert response.status_code == 201
    assert response.json()["tags"] == ["backend", "urgent"]


def test_create_task_dedupes_and_trims_tags(client):
    response = client.post(
        "/tasks", json={"title": "Task", "tags": [" backend ", "backend", "urgent"]}
    )

    assert response.status_code == 201
    assert response.json()["tags"] == ["backend", "urgent"]


def test_create_task_with_blank_tag_returns_422(client):
    response = client.post("/tasks", json={"title": "Task", "tags": ["valid", "   "]})

    assert response.status_code == 422


def test_create_task_with_too_many_tags_returns_422(client):
    response = client.post(
        "/tasks", json={"title": "Task", "tags": [f"tag{i}" for i in range(11)]}
    )

    assert response.status_code == 422


def test_create_task_with_tag_too_long_returns_422(client):
    response = client.post("/tasks", json={"title": "Task", "tags": ["x" * 31]})

    assert response.status_code == 422


def test_update_tags_replaces_list(client, created_task):
    task_id = created_task["id"]

    response = client.patch(f"/tasks/{task_id}", json={"tags": ["frontend"]})

    assert response.status_code == 200
    assert response.json()["tags"] == ["frontend"]


def test_update_tags_with_blank_tag_returns_422(client, created_task):
    task_id = created_task["id"]

    response = client.patch(f"/tasks/{task_id}", json={"tags": [""]})

    assert response.status_code == 422


def test_patch_unrelated_field_preserves_tags(client):
    created = client.post(
        "/tasks", json={"title": "Task", "tags": ["backend"]}
    ).json()

    response = client.patch(f"/tasks/{created['id']}", json={"status": "InProgress"})

    assert response.status_code == 200
    assert response.json()["tags"] == ["backend"]


def test_list_tasks_filter_by_tag_returns_only_matches(client):
    client.post("/tasks", json={"title": "Task 1", "tags": ["backend"]})
    client.post("/tasks", json={"title": "Task 2", "tags": ["frontend"]})
    client.post("/tasks", json={"title": "Task 3"})

    response = client.get("/tasks", params={"tag": "backend"})

    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Task 1"


def test_list_tasks_filter_by_tag_is_case_insensitive(client):
    client.post("/tasks", json={"title": "Task 1", "tags": ["Backend"]})

    response = client.get("/tasks", params={"tag": "backend"})

    assert response.status_code == 200
    assert len(response.json()) == 1
