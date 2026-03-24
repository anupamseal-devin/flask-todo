Simple Flask Todo App using SQLAlchemy and SQLite database.

For styling [semantic-ui](https://semantic-ui.com/) is used.

### Project Structure

```
app/
├── __init__.py          # Flask app factory (create_app)
├── models/
│   └── todo.py          # Todo SQLAlchemy model
├── routes/
│   ├── views.py         # HTML routes (home/add/update/delete)
│   └── api.py           # REST API endpoints (JSON)
├── services/
│   └── todo_service.py  # Business logic layer
├── schemas/
│   └── todo_schema.py   # Marshmallow schemas for validation
└── templates/
    └── base.html        # Jinja2 template
run.py                   # Entry point
tests/
├── test_todo_api.py     # API endpoint tests
└── test_todo_service.py # Service layer unit tests
```

### Setup

Create project with virtual environment

```console
$ python3 -m venv venv
```

Activate it
```console
$ . venv/bin/activate
```

or on Windows
```console
venv\Scripts\activate
```

Install dependencies
```console
$ pip install -r requirements.txt
```

Copy and configure environment variables (optional — defaults are provided)
```console
$ cp .env.example .env
```

### Running the App

```console
$ python run.py
```

The app will be available at `http://localhost:5000`.

### REST API

| Method | Endpoint             | Description                  |
|--------|----------------------|------------------------------|
| GET    | `/api/todos`         | List all todos (JSON)        |
| POST   | `/api/todos`         | Create a todo (`{"title": "..."}`) |
| PUT    | `/api/todos/<id>`    | Toggle complete status       |
| DELETE | `/api/todos/<id>`    | Delete a todo                |

### Running Tests

```console
$ pytest
```
