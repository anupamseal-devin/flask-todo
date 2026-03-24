from flask import Blueprint, redirect, render_template, request, url_for

from app.services.todo_service import TodoService

views_bp = Blueprint("views", __name__)


@views_bp.route("/")
def home():
    todo_list = TodoService.get_all()
    return render_template("base.html", todo_list=todo_list)


@views_bp.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    try:
        TodoService.create(title)
    except ValueError:
        pass  # Silently ignore invalid input from the form (matches original behaviour)
    return redirect(url_for("views.home"))


@views_bp.route("/update/<int:todo_id>")
def update(todo_id):
    try:
        TodoService.toggle_complete(todo_id)
    except ValueError:
        pass
    return redirect(url_for("views.home"))


@views_bp.route("/delete/<int:todo_id>")
def delete(todo_id):
    try:
        TodoService.delete(todo_id)
    except ValueError:
        pass
    return redirect(url_for("views.home"))
