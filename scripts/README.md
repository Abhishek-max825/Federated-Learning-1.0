# `scripts/` — Database Seeding & Utilities

Scripts for setting up and inspecting the application database.

## Files

| File             | Purpose                                        |
|------------------|------------------------------------------------|
| `seed.py`        | Seeds the database with roles, hospitals, and default users |
| `check_users.py` | Quick utility to list all users and their roles |

## Seeding (`seed.py`)

Run this to populate the database with initial data:

```bash
python scripts/seed.py
```

**Creates:**
1. **3 Roles**: Admin, Doctor, Hospital Node
2. **3 Hospitals**: Hospital Node 1 (Location A), Hospital Node 2 (Location B), Hospital Node 3 (Location C)
3. **1 Admin user**: `admin` / `admin123`
4. **1 Doctor user**: `doctor` / `doctor123`
5. **3 Hospital users**: 
   - `hospital` / `hospital123` → Hospital Node 1
   - `hospital2` / `hospital2123` → Hospital Node 2
   - `hospital3` / `hospital3123` → Hospital Node 3

The script is **idempotent** — running it again won't duplicate data. It also fixes existing hospital users that are missing their `hospital_id` link.

## Checking Users (`check_users.py`)

```bash
python scripts/check_users.py
```

Lists all users with their username, email, role, and linked hospital.
