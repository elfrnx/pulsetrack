# PulseTrack

Lab project for the **Data as a Service (DAAS)** course at Thomas More, week 2: PulseTrack on a SQL database.

PulseTrack is a REST API for sports activities, built with FastAPI on SQLite. It supports full CRUD on activities and users, filtering and pagination, and the data survives a server restart.

## Run

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python create_db.py
fastapi dev main.py
```

Open http://127.0.0.1:8000/docs

## Files

- `main.py` – HTTP: endpoints and status codes (no SQL)
- `schemas.py` – Pydantic shapes of the data in and out
- `database.py` – all the SQL (no HTTP)
- `pulsetrack.sql` + `create_db.py` – build a fresh `pulsetrack.db` (5 users, 16 activities)

## Endpoints

| Method | Path | Success | Errors |
|---|---|---|---|
| GET | `/activities?sport=&limit=&offset=` | 200 | 422 |
| GET | `/activities/{id}` | 200 | 404, 422 |
| POST | `/activities` | 201 + Location | 404, 422 |
| PUT | `/activities/{id}` | 200 | 404, 422 |
| DELETE | `/activities/{id}` | 204 | 404 |
| GET | `/users` | 200 | |
| GET | `/users/{id}` | 200 | 404 |
| POST | `/users` | 201 + Location | 409, 422 |
| DELETE | `/users/{id}` | 204 | 404 |
| GET | `/users/{id}/activities` | 200 | 404 |
