import json

import pytest

from app import create_app, db


@pytest.fixture()
def app():
    app = create_app(testing=True)
    with app.app_context():
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


class TestGetTodos:
    def test_returns_empty_list(self, client):
        resp = client.get("/api/todos")
        assert resp.status_code == 200
        assert resp.get_json() == []

    def test_returns_all_todos(self, client):
        client.post("/api/todos", json={"title": "First"})
        client.post("/api/todos", json={"title": "Second"})
        resp = client.get("/api/todos")
        data = resp.get_json()
        assert len(data) == 2
        assert data[0]["title"] == "First"
        assert data[1]["title"] == "Second"


class TestCreateTodo:
    def test_creates_todo(self, client):
        resp = client.post("/api/todos", json={"title": "Buy milk"})
        assert resp.status_code == 201
        data = resp.get_json()
        assert data["title"] == "Buy milk"
        assert data["complete"] is False
        assert "id" in data

    def test_rejects_missing_body(self, client):
        resp = client.post("/api/todos", content_type="application/json")
        assert resp.status_code == 400

    def test_rejects_missing_title(self, client):
        resp = client.post("/api/todos", json={"description": "no title"})
        assert resp.status_code == 400
        assert "title" in resp.get_json()["error"].lower()

    def test_rejects_empty_title(self, client):
        resp = client.post("/api/todos", json={"title": ""})
        assert resp.status_code == 400

    def test_rejects_title_over_100_chars(self, client):
        resp = client.post("/api/todos", json={"title": "a" * 101})
        assert resp.status_code == 400


class TestUpdateTodo:
    def test_toggles_complete(self, client):
        create_resp = client.post("/api/todos", json={"title": "Test"})
        todo_id = create_resp.get_json()["id"]

        resp = client.put(f"/api/todos/{todo_id}")
        assert resp.status_code == 200
        assert resp.get_json()["complete"] is True

        resp = client.put(f"/api/todos/{todo_id}")
        assert resp.status_code == 200
        assert resp.get_json()["complete"] is False

    def test_returns_404_for_nonexistent(self, client):
        resp = client.put("/api/todos/9999")
        assert resp.status_code == 404


class TestDeleteTodo:
    def test_deletes_todo(self, client):
        create_resp = client.post("/api/todos", json={"title": "Test"})
        todo_id = create_resp.get_json()["id"]

        resp = client.delete(f"/api/todos/{todo_id}")
        assert resp.status_code == 204

        get_resp = client.get("/api/todos")
        assert get_resp.get_json() == []

    def test_returns_404_for_nonexistent(self, client):
        resp = client.delete("/api/todos/9999")
        assert resp.status_code == 404
