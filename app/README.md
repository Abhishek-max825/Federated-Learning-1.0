# `app/` — Main Flask Application Package

This is the core application package. Flask uses the **Application Factory** pattern via `create_app()` in `__init__.py`.

## Structure

```
app/
├── __init__.py         # App factory: creates Flask app, initializes extensions, registers blueprints
├── models.py           # SQLAlchemy models (User, Role, Hospital, AuditLog, ModelVersion)
├── decorators.py       # @admin_required, @doctor_required, @hospital_required
├── fl_globals.py       # Singleton FLAggregator instance shared across the app
├── api/                # REST API blueprint (/api/...)
├── auth/               # Authentication blueprint (/auth/...)
├── fl/                 # Federated Learning engine (not a blueprint — pure Python)
├── main/               # Main pages blueprint (/, /admin, /doctor, /hospital)
├── static/             # Static assets (CSS)
├── templates/          # Jinja2 HTML templates
└── uploads/            # Runtime directory for uploaded CSV files
```

## Key Files

### `__init__.py` — Application Factory
- Initializes `SQLAlchemy`, `Flask-Migrate`, `Flask-Login`
- Registers 3 blueprints: `auth`, `main`, `api`
- Handles unauthorized API requests with JSON responses

### `models.py` — Database Models
| Model         | Purpose                                      |
|---------------|----------------------------------------------|
| `Role`        | User roles: Admin, Doctor, Hospital Node     |
| `Hospital`    | Hospital entities with name & location       |
| `User`        | Users linked to a Role and optionally a Hospital |
| `AuditLog`    | Tracks FL training events and admin actions  |
| `ModelVersion` | Stores global model version history          |

### `decorators.py` — Role-Based Access Control
Provides `@admin_required`, `@doctor_required`, `@hospital_required` decorators that check `current_user.role.name` and return 403 if unauthorized.

### `fl_globals.py`
Creates a single `FLAggregator` instance that persists across requests, holding the global model state and client updates.
