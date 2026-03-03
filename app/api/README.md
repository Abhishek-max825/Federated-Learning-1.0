# `app/api/` — REST API Blueprint

Handles all API endpoints under the `/api/` prefix. These power the AJAX-driven interactions on the dashboards.

## Files

| File            | Purpose                            |
|-----------------|-------------------------------------|
| `__init__.py`   | Creates the `api` Blueprint        |
| `routes.py`     | All API route handlers             |

## Endpoints

### Federated Learning

| Method | Endpoint              | Auth Required | Role      | Description                          |
|--------|-----------------------|---------------|-----------|--------------------------------------|
| GET    | `/api/fl/status`      | ✅            | Any       | Current FL round & client count      |
| POST   | `/api/fl/start_round` | ✅            | Admin     | Start a new FL training round        |
| POST   | `/api/fl/train`       | ✅            | Hospital  | Upload CSV & train local model       |
| POST   | `/api/fl/aggregate`   | ✅            | Admin     | Aggregate client updates (FedAvg)    |
| GET    | `/api/fl/history`     | ✅            | Any       | Training history (rounds, metrics)   |
| POST   | `/api/fl/evaluate`    | ✅            | Admin     | Evaluate global model on test data   |
| POST   | `/api/fl/rollback/<n>`| ✅            | Admin     | Rollback to a previous round's model |
| POST   | `/api/fl/reset`       | ✅            | Admin     | Reset all FL state                   |

### User Management

| Method | Endpoint               | Auth Required | Role  | Description          |
|--------|------------------------|---------------|-------|----------------------|
| GET    | `/api/users`           | ✅            | Admin | List all users       |
| POST   | `/api/users`           | ✅            | Admin | Create a new user    |
| DELETE | `/api/users/<id>`      | ✅            | Admin | Delete a user        |
| DELETE | `/api/audit-logs`      | ✅            | Admin | Clear audit logs     |

## Training Flow (`/api/fl/train`)

1. Hospital uploads a CSV file via `multipart/form-data`
2. File is saved to `app/uploads/`
3. `FLClient` loads & preprocesses the data using `FLDataHandler`
4. Local model trains for 5 epochs on the data
5. Trained weights + differential privacy noise are sent to the `FLAggregator`
6. Training event is logged to `AuditLog`
7. Returns metrics (accuracy, loss, sample count) as JSON
