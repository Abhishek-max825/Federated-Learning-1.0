# 🫀 Heart Disease FL — Federated Learning System

A privacy-preserving **Federated Learning** web application for heart disease prediction using the BRFSS 2022 dataset. Multiple hospital nodes train local models on their private data and send only model weight updates to a central server, which aggregates them into a stronger global model — **without ever sharing raw patient data**.

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                   Flask Web App                      │
│  ┌──────────┐  ┌──────────┐  ┌───────────────────┐  │
│  │   Auth   │  │   Main   │  │       API         │  │
│  │ (login,  │  │ (dashbd, │  │  (FL train,       │  │
│  │ register)│  │ predict) │  │  aggregate, mgmt) │  │
│  └──────────┘  └──────────┘  └───────────────────┘  │
│                      │                               │
│              ┌───────┴───────┐                       │
│              │   FL Engine   │                       │
│              │ model, client │                       │
│              │ data, aggreg. │                       │
│              └───────────────┘                       │
└─────────────────────────────────────────────────────┘
```

## Tech Stack

| Layer        | Technology                                       |
|------------- |--------------------------------------------------|
| Backend      | Flask, Flask-Login, Flask-Migrate, SQLAlchemy     |
| ML/DL        | PyTorch (DNN), scikit-learn (preprocessing)       |
| Database     | SQLite                                           |
| Frontend     | Bootstrap 5 (dark mode), Toastify.js             |
| Data Source  | BRFSS 2022 (CDC Behavioral Risk Factor Survey)    |

## Project Structure

```
Federated_Learning/
├── app/                    # Main Flask application package
│   ├── api/                # REST API endpoints (FL training, user mgmt)
│   ├── auth/               # Authentication (login, register, logout)
│   ├── fl/                 # Federated Learning engine (model, client, data, aggregator)
│   ├── main/               # Page routes & doctor prediction form
│   ├── static/             # CSS stylesheets
│   ├── templates/          # Jinja2 HTML templates
│   ├── uploads/            # Uploaded CSV datasets (runtime)
│   ├── models.py           # SQLAlchemy database models
│   ├── decorators.py       # Role-based access control decorators
│   └── fl_globals.py       # Global FL aggregator instance
├── heart_disease_dataset/  # BRFSS 2022 source data & hospital sub-datasets
├── scripts/                # Database seeding & utility scripts
├── tests/                  # Verification & test scripts
├── migrations/             # Alembic database migrations
├── config.py               # Flask configuration
├── run.py                  # Application entry point
└── requirements.txt        # Python dependencies
```

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Seed the database (creates roles, hospitals, users)
python scripts/seed.py

# 3. Run the dev server
flask run --debug --no-reload
```

## User Roles & Credentials (Seeded)

| Role          | Username    | Password       | Access                          |
|---------------|-------------|----------------|----------------------------------|
| Admin         | `admin`     | `admin123`     | User mgmt, FL rounds, aggregation |
| Doctor        | `doctor`    | `doctor123`    | Heart disease prediction         |
| Hospital Node | `hospital`  | `hospital123`  | Local training (Node 1)          |
| Hospital Node | `hospital2` | `hospital2123` | Local training (Node 2)          |
| Hospital Node | `hospital3` | `hospital3123` | Local training (Node 3)          |

## Federated Learning Workflow

1. **Admin** starts a new FL round
2. **Hospital nodes** upload their CSV datasets and train local models
3. Each node sends model weight updates (not raw data) to the server
4. **Admin** triggers aggregation (FedAvg) to update the global model
5. **Doctors** use the global model for heart disease prediction
