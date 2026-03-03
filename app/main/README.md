# `app/main/` — Main Pages Blueprint

Serves the primary page routes (no URL prefix — mounted at root `/`).

## Files

| File          | Purpose                                       |
|---------------|-----------------------------------------------|
| `__init__.py` | Creates the `main` Blueprint                  |
| `routes.py`   | Page route handlers for all dashboards        |
| `forms.py`    | `PredictionForm` (WTForms) for doctor's heart disease prediction |

## Routes

| Method    | Endpoint              | Role     | Description                        |
|-----------|-----------------------|----------|------------------------------------|
| GET       | `/` or `/index`       | Any      | Home page — redirects to role dashboard |
| GET       | `/admin/dashboard`    | Admin    | Admin panel: FL rounds, user mgmt, audit logs |
| GET/POST  | `/doctor/dashboard`   | Doctor   | Heart disease prediction form      |
| GET       | `/hospital/dashboard` | Hospital | Local training interface           |

## Doctor Prediction Form (`forms.py`)

The `PredictionForm` collects patient data for heart disease prediction:
- **Age Group** (1-6 BRFSS scale)
- **Sex** (Male/Female)
- **BMI** (decimal, e.g., 25.5 — automatically scaled ×100 for BRFSS format)
- **Smoking history**, **Diabetes**, **Heart attack history**, **Stroke history**

The form data is preprocessed through `FLDataHandler` and fed into the global model for prediction.
