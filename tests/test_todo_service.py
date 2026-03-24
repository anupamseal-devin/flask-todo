import pytest

from app import create_app, db
from app.models.todo import Todo
from app.services.todo_service import TodoService


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


class TestTodoServiceGetAll:
    def test_returns_empty_list_when_no_todos(self, app):
        with app.app_context():
            assert TodoService.get_all() == []

    def test_returns_all_todos(self, app):
        with app.app_context():
            TodoService.create("First")
            TodoService.create("Second")
            todos = TodoService.get_all()
            assert len(todos) == 2
            assert todos[0].title == "First"
            assert todos[1].title == "Second"


class TestTodoServiceCreate:
    def test_creates_todo(self, app):
        with app.app_context():
            todo = TodoService.create("Buy milk")
            assert todo.id is not None
            assert todo.title == "Buy milk"
            assert todo.complete is False

    def test_strips_whitespace(self, app):
        with app.app_context():
            todo = TodoService.create("  Buy milk  ")
            assert todo.title == "Buy milk"

    def test_rejects_empty_title(self, app):
        with app.app_context():
            with pytest.raises(ValueError, match="must not be empty"):
                TodoService.create("")

    def test_rejects_whitespace_only_title(self, app):
        with app.app_context():
            with pytest.raises(ValueError, match="must not be empty"):
                TodoService.create("   ")

    def test_rejects_none_title(self, app):
        with app.app_context():
            with pytest.raises(ValueError, match="must not be empty"):
                TodoService.create(None)

    def test_rejects_title_over_100_chars(self, app):
        with app.app_context():
            with pytest.raises(ValueError, match="must not exceed 100 characters"):
                TodoService.create("a" * 101)

    def test_accepts_title_exactly_100_chars(self, app):
        with app.app_context():
            todo = TodoService.create("a" * 100)
            assert len(todo.title) == 100


class TestTodoServiceToggleComplete:
    def test_toggles_incomplete_to_complete(self, app):
        with app.app_context():
            todo = TodoService.create("Test")
            assert todo.complete is False
            updated = TodoService.toggle_complete(todo.id)
            assert updated.complete is True

    def test_toggles_complete_to_incomplete(self, app):
        with app.app_context():
            todo = TodoService.create("Test")
            TodoService.toggle_complete(todo.id)
            updated = TodoService.toggle_complete(todo.id)
            assert updated.complete is False

    def test_raises_for_nonexistent_id(self, app):
        with app.app_context():
            with pytest.raises(ValueError, match="not found"):
                TodoService.toggle_complete(9999)


class TestTodoServiceDelete:
    def test_deletes_todo(self, app):
        with app.app_context():
            todo = TodoService.create("Test")
            TodoService.delete(todo.id)
            assert TodoService.get_all() == []

    def test_raises_for_nonexistent_id(self, app):
        with app.app_context():
            with pytest.raises(ValueError, match="not found"):
                TodoService.delete(9999)
