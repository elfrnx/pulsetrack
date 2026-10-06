# PulseTrack

DAAS week 2 lab: a REST API with FastAPI on a SQLite database.

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
