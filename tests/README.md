# `tests/` — Verification & Test Scripts

Test scripts for verifying different aspects of the application.

## Files

| File                       | Tests                                           |
|---------------------------|--------------------------------------------------|
| `test_advanced_fl.py`     | End-to-end FL training, aggregation, rollback    |
| `test_delete.py`          | User deletion functionality                      |
| `verify_login.py`         | Login flow and authentication                    |
| `verify_registration.py`  | User registration for different roles            |
| `verify_rbac.py`          | Role-Based Access Control (403 for wrong roles)  |
| `verify_admin_actions.py` | Admin dashboard actions (FL rounds, user mgmt)   |
| `verify_fl.py`            | Federated Learning API endpoints                 |
| `verify_enhancements.py`  | UI and feature enhancements                      |
| `verify_ui.py`            | UI rendering and template checks                 |
| `verify_user_mgmt.py`     | User CRUD via API                                |

## Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run a specific test
python tests/verify_login.py
```

## What's Covered

- **Authentication**: Login, logout, registration, session handling
- **Authorization**: RBAC — Admin/Doctor/Hospital routes return 403 for wrong roles
- **FL Pipeline**: Training → aggregation → rollback → reset
- **User Management**: Create, list, delete users via admin API
- **UI**: Template rendering, dashboard content
