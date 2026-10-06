"""The HTTP side of PulseTrack: receive the request, ask database.py, answer."""

from fastapi import FastAPI, HTTPException, Query, Response

import database as db
from schemas import ActivityCreate, ActivityRead, ActivityUpdate, Sport, UserCreate, UserRead

app = FastAPI(title="PulseTrack")


@app.get("/")
def read_root():
    return {"message": "Welcome to PulseTrack"}


# ---------- activities ----------

@app.get("/activities", response_model=list[ActivityRead], tags=["activities"])
def list_activities(
    sport: Sport | None = None,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    return db.list_activities(sport, limit, offset)


@app.get("/activities/{activity_id}", response_model=ActivityRead, tags=["activities"])
def read_activity(activity_id: int):
    activity = db.get_activity(activity_id)
    if activity is None:
        raise HTTPException(status_code=404, detail=f"Activity {activity_id} not found")
    return activity


@app.post("/activities", response_model=ActivityRead, status_code=201, tags=["activities"])
def create_activity(data: ActivityCreate, response: Response):
    if db.get_user(data.user_id) is None:
        raise HTTPException(status_code=404, detail=f"User {data.user_id} not found")
    activity = db.create_activity(data.model_dump(mode="json"))
    response.headers["Location"] = f"/activities/{activity['id']}"
    return activity


@app.put("/activities/{activity_id}", response_model=ActivityRead, tags=["activities"])
def replace_activity(activity_id: int, data: ActivityUpdate):
    if db.get_activity(activity_id) is None:
        raise HTTPException(status_code=404, detail=f"Activity {activity_id} not found")
    return db.update_activity(activity_id, data.model_dump(mode="json"))


@app.delete("/activities/{activity_id}", status_code=204, tags=["activities"])
def delete_activity(activity_id: int):
    if db.get_activity(activity_id) is None:
        raise HTTPException(status_code=404, detail=f"Activity {activity_id} not found")
    db.delete_activity(activity_id)


# ---------- users ----------

@app.get("/users", response_model=list[UserRead], tags=["users"])
def list_users():
    return db.list_users()


@app.get("/users/{user_id}", response_model=UserRead, tags=["users"])
def read_user(user_id: int):
    user = db.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return user


@app.post("/users", response_model=UserRead, status_code=201, tags=["users"])
def create_user(data: UserCreate, response: Response):
    if db.get_user_by_email(data.email) is not None:
        raise HTTPException(status_code=409, detail=f"E-mail {data.email} is already registered")
    user = db.create_user(data.model_dump())
    response.headers["Location"] = f"/users/{user['id']}"
    return user


@app.delete("/users/{user_id}", status_code=204, tags=["users"])
def delete_user(user_id: int):
    if db.get_user(user_id) is None:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    db.delete_user(user_id)


@app.get("/users/{user_id}/activities", response_model=list[ActivityRead], tags=["users"])
def list_activities_of_user(user_id: int):
    if db.get_user(user_id) is None:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return db.list_activities_of_user(user_id)
