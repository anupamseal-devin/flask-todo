from flask import Blueprint, request, jsonify

from models import db
from models.todo import Todo

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/todos", methods=["GET"])
def get_todos():
    todos = Todo.query.all()
    return jsonify(
        [
            {"id": t.id, "title": t.title, "complete": t.complete}
            for t in todos
        ]
    )


@api_bp.route("/todos", methods=["POST"])
def create_todo():
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    if not title or not str(title).strip():
        return jsonify({"error": "title is required"}), 400
    new_todo = Todo(title=str(title).strip(), complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return jsonify(
        {"id": new_todo.id, "title": new_todo.title, "complete": new_todo.complete}
    ), 201


@api_bp.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    if not todo:
        return jsonify({"error": "todo not found"}), 404
    data = request.get_json(silent=True) or {}
    if "title" in data:
        if not data["title"] or not str(data["title"]).strip():
            return jsonify({"error": "title cannot be empty"}), 400
        todo.title = str(data["title"]).strip()
    if "complete" in data:
        todo.complete = data["complete"]
    db.session.commit()
    return jsonify(
        {"id": todo.id, "title": todo.title, "complete": todo.complete}
    )


@api_bp.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    if not todo:
        return jsonify({"error": "todo not found"}), 404
    db.session.delete(todo)
    db.session.commit()
    return jsonify({"message": "todo deleted"})
