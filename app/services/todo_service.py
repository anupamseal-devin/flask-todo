from app import db
from app.models.todo import Todo


class TodoService:
    """Service layer encapsulating all Todo business logic."""

    @staticmethod
    def get_all():
        """Return all todos ordered by id."""
        return Todo.query.order_by(Todo.id).all()

    @staticmethod
    def create(title):
        """Create a new todo after validating the title.

        Args:
            title: The todo title string.

        Returns:
            The newly created Todo instance.

        Raises:
            ValueError: If title is empty or exceeds 100 characters.
        """
        if not title or not title.strip():
            raise ValueError("Title must not be empty.")
        title = title.strip()
        if len(title) > 100:
            raise ValueError("Title must not exceed 100 characters.")

        todo = Todo(title=title, complete=False)
        db.session.add(todo)
        db.session.commit()
        return todo

    @staticmethod
    def toggle_complete(todo_id):
        """Toggle the complete status of a todo.

        Args:
            todo_id: The integer id of the todo.

        Returns:
            The updated Todo instance.

        Raises:
            ValueError: If the todo is not found.
        """
        todo = db.session.get(Todo, todo_id)
        if todo is None:
            raise ValueError(f"Todo with id {todo_id} not found.")
        todo.complete = not todo.complete
        db.session.commit()
        return todo

    @staticmethod
    def delete(todo_id):
        """Delete a todo by id.

        Args:
            todo_id: The integer id of the todo.

        Raises:
            ValueError: If the todo is not found.
        """
        todo = db.session.get(Todo, todo_id)
        if todo is None:
            raise ValueError(f"Todo with id {todo_id} not found.")
        db.session.delete(todo)
        db.session.commit()
