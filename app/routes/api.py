from flask import Blueprint, jsonify, request

from app.services.todo_service import TodoService

api_bp = Blueprint("api", __name__)


@api_bp.route("/todos", methods=["GET"])
def get_todos():
    """Return a JSON list of all todos."""
    todos = TodoService.get_all()
    return jsonify([todo.to_dict() for todo in todos])


@api_bp.route("/todos", methods=["POST"])
def create_todo():
    """Create a new todo from JSON body ``{"title": "..."}``."""
    data = request.get_json(silent=True)
    if not data or "title" not in data:
        return jsonify({"error": "Request body must include a 'title' field."}), 400

    try:
        todo = TodoService.create(data["title"])
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify(todo.to_dict()), 201


@api_bp.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    """Toggle the complete status of a todo."""
    try:
        todo = TodoService.toggle_complete(todo_id)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 404

    return jsonify(todo.to_dict())


@api_bp.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    """Delete a todo by id."""
    try:
        TodoService.delete(todo_id)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 404

    return "", 204
