"""The shapes of the data that enters and leaves the API (Pydantic)."""

from typing import Literal

from pydantic import AwareDatetime, BaseModel, EmailStr, Field

Sport = Literal["run", "ride", "swim", "gym"]


class ActivityRead(BaseModel):               # every response that shows an activity
    id: int
    user_id: int
    sport: Sport
    title: str
    started_at: AwareDatetime
    duration_s: int
    distance_m: float


class ActivityCreate(BaseModel):             # body of POST /activities
    user_id: int
    sport: Sport
    title: str = Field(min_length=1, max_length=100)
    started_at: AwareDatetime
    duration_s: int = Field(gt=0)
    distance_m: float = Field(default=0, ge=0)


class ActivityUpdate(BaseModel):             # body of PUT /activities/{id}
    sport: Sport
    title: str = Field(min_length=1, max_length=100)
    started_at: AwareDatetime
    duration_s: int = Field(gt=0)
    distance_m: float = Field(default=0, ge=0)


class UserCreate(BaseModel):                 # no id, no role
    email: EmailStr
    display_name: str = Field(min_length=2, max_length=50)


class UserRead(BaseModel):
    id: int
    email: EmailStr
    display_name: str
