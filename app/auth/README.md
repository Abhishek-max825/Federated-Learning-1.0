# `app/auth/` — Authentication Blueprint

Handles user authentication under the `/auth/` prefix.

## Files

| File            | Purpose                                  |
|-----------------|------------------------------------------|
| `__init__.py`   | Creates the `auth` Blueprint             |
| `routes.py`     | Login, logout, and registration routes   |
| `forms.py`      | WTForms: `LoginForm`, `RegistrationForm` |

## Routes

| Method    | Endpoint          | Description                                |
|-----------|-------------------|--------------------------------------------|
| GET/POST  | `/auth/login`     | Login page with role-based redirect        |
| GET       | `/auth/logout`    | Logs out user and redirects to home        |
| GET/POST  | `/auth/register`  | Self-registration for Doctor/Hospital roles |

## Login Redirect Logic

After login, users are redirected based on their role:
- **Admin** → `/admin/dashboard`
- **Doctor** → `/doctor/dashboard`
- **Hospital Node** → `/hospital/dashboard`

## Registration

New users can register with either the **Doctor** or **Hospital Node** role (Admin accounts are seeded only).
