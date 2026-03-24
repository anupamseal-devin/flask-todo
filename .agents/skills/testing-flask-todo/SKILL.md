# Testing the Flask Todo App

## Prerequisites
- Python 3.12+ with a virtual environment set up at `venv/`
- Dependencies installed: `pip install -r requirements.txt`

## Running the App Locally

1. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```
2. Start the dev server:
   ```bash
   python run.py
   ```
   The app runs at `http://127.0.0.1:5000`.

3. If port 5000 is already in use, kill the existing process first:
   ```bash
   fuser -k 5000/tcp
   ```

## Running the Test Suite

```bash
source venv/bin/activate && pytest tests/ -v
```

Tests use an in-memory SQLite database (configured via `create_app(testing=True)`), so no external DB setup is needed.

## Testing the HTML UI (Browser)

Navigate to `http://127.0.0.1:5000` in a browser.

- **Create**: Type a title in the input field and click "Add". The todo appears as a segment with `<id> | <title>`, a gray "Not Complete" label, blue "Update" button, and red "Delete" button.
- **Toggle complete**: Click "Update" on a todo. The label toggles between "Not Complete" (gray) and "Completed" (green).
- **Delete**: Click "Delete" on a todo. The segment disappears.

The HTML routes use `url_for("views.home")` for redirects. If blueprint registration changes, verify form actions in `app/templates/base.html` still point to `/add`, `/update/<id>`, `/delete/<id>`.

## Testing the REST API (curl)

All API endpoints are under `/api/` prefix:

```bash
# List all todos
curl -s http://127.0.0.1:5000/api/todos

# Create a todo (expects JSON with "title" string field)
curl -s -X POST -H "Content-Type: application/json" -d '{"title":"Test"}' http://127.0.0.1:5000/api/todos

# Toggle complete status
curl -s -X PUT http://127.0.0.1:5000/api/todos/1

# Delete a todo
curl -s -X DELETE http://127.0.0.1:5000/api/todos/1
```

### Expected Status Codes
- `GET /api/todos` → 200
- `POST /api/todos` → 201 (success), 400 (invalid input)
- `PUT /api/todos/<id>` → 200 (success), 404 (not found)
- `DELETE /api/todos/<id>` → 204 (success), 404 (not found)

### Validation Edge Cases to Test
- Empty body → 400
- Empty title `{"title": ""}` → 400
- Non-string title `{"title": 123}` → 400
- Title > 100 chars → 400
- Nonexistent ID for PUT/DELETE → 404

## Architecture Notes

- App uses the factory pattern (`create_app()` in `app/__init__.py`)
- Business logic is in `app/services/todo_service.py` — route handlers delegate to the service layer
- `db.create_all()` runs automatically on `create_app()` so no manual DB init is needed
- CORS is enabled with default (allow-all) settings via `flask-cors`
- The SQLite database file is created at `instance/db.sqlite` by default

## Devin Secrets Needed
None — this app uses local SQLite and requires no external credentials.
