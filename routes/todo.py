from flask import Blueprint, render_template, request, redirect, url_for

from models import db
from models.todo import Todo

todo_bp = Blueprint("todo", __name__)


@todo_bp.route("/")
def home():
    todo_list = Todo.query.all()
    return render_template("base.html", todo_list=todo_list)


@todo_bp.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    if not title or not title.strip():
        return redirect(url_for("todo.home"))
    new_todo = Todo(title=title.strip(), complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("todo.home"))


@todo_bp.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("todo.home"))


@todo_bp.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("todo.home"))
