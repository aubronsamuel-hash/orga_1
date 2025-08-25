import re
from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


# --- Users (J3) ---

class UserCreate(BaseModel):
    model_config = ConfigDict(strict=True)
    email: str = Field(...)
    password: str = Field(min_length=8)

    @field_validator("email")
    @classmethod
    def _email(cls, v: str) -> str:
        if not EMAIL_RE.match(v):
            raise ValueError("email invalide")
        return v.lower()


class UserOut(BaseModel):
    model_config = ConfigDict(strict=True, from_attributes=True)
    id: int
    email: str
    is_active: bool
    is_admin: bool
    totp_enabled: bool
    created_at: datetime


class UserUpdate(BaseModel):
    model_config = ConfigDict(strict=True)
    is_active: bool | None = None
    is_admin: bool | None = None


class TokenPair(BaseModel):
    model_config = ConfigDict(strict=True)
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class LoginIn(BaseModel):
    model_config = ConfigDict(strict=True)
    email: str
    password: str
    totp_code: str | None = None


# --- Missions (J4) ---

def _norm_dt(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=UTC)
    return dt.astimezone(UTC)


class MissionBase(BaseModel):
    model_config = ConfigDict()
    title: str = Field(min_length=2)
    location: str | None = None
    start_at: datetime
    end_at: datetime
    description: str | None = None

    @field_validator("start_at", "end_at", mode="before")
    @classmethod
    def _ensure_tz(cls, v: datetime | str) -> datetime:
        if isinstance(v, str):
            v = datetime.fromisoformat(v)
        return _norm_dt(v)

    @field_validator("end_at")
    @classmethod
    def _end_after_start(cls, v: datetime, info):
        start = info.data.get("start_at")
        if isinstance(start, datetime) and _norm_dt(v) <= _norm_dt(start):
            raise ValueError("end_at doit etre > start_at")
        return v


class MissionCreate(MissionBase):
    pass


class MissionUpdate(BaseModel):
    model_config = ConfigDict()
    title: str | None = None
    location: str | None = None
    start_at: datetime | None = None
    end_at: datetime | None = None
    description: str | None = None

    @field_validator("start_at", "end_at", mode="before")
    @classmethod
    def _ensure_tz(cls, v: datetime | str | None) -> datetime | None:
        if v is None:
            return None
        if isinstance(v, str):
            v = datetime.fromisoformat(v)
        return _norm_dt(v)

    @field_validator("end_at")
    @classmethod
    def _end_after_start(cls, v: datetime | None, info):
        start = info.data.get("start_at")
        if v is not None and start is not None and _norm_dt(v) <= _norm_dt(start):
            raise ValueError("end_at doit etre > start_at")
        return v


class MissionOut(MissionBase):
    model_config = ConfigDict(strict=True, from_attributes=True)
    id: int


class MissionDetail(MissionOut):
    roles: list["MissionRoleOut"] = []
    assignments: list["AssignmentOut"] = []


class MissionRoleCreate(BaseModel):
    model_config = ConfigDict()
    name: str = Field(min_length=2)
    start_at: datetime | None = None
    end_at: datetime | None = None
    quantity: int = Field(default=1, ge=1)

    @field_validator("start_at", "end_at", mode="before")
    @classmethod
    def _ensure_tz(cls, v: datetime | str | None) -> datetime | None:
        if v is None:
            return None
        if isinstance(v, str):
            v = datetime.fromisoformat(v)
        return _norm_dt(v)

    @field_validator("end_at")
    @classmethod
    def _end_after_start(cls, v: datetime | None, info):
        start = info.data.get("start_at")
        if v is not None and start is not None and _norm_dt(v) <= _norm_dt(start):
            raise ValueError("end_at doit etre > start_at")
        return v


class MissionRoleUpdate(BaseModel):
    model_config = ConfigDict()
    name: str | None = None
    start_at: datetime | None = None
    end_at: datetime | None = None
    quantity: int | None = Field(default=None, ge=1)

    @field_validator("start_at", "end_at", mode="before")
    @classmethod
    def _ensure_tz(cls, v: datetime | str | None) -> datetime | None:
        if v is None:
            return None
        if isinstance(v, str):
            v = datetime.fromisoformat(v)
        return _norm_dt(v)

    @field_validator("end_at")
    @classmethod
    def _end_after_start(cls, v: datetime | None, info):
        start = info.data.get("start_at")
        if v is not None and start is not None and _norm_dt(v) <= _norm_dt(start):
            raise ValueError("end_at doit etre > start_at")
        return v


class MissionRoleOut(BaseModel):
    model_config = ConfigDict(strict=True, from_attributes=True)
    id: int
    mission_id: int
    name: str
    start_at: datetime | None = None
    end_at: datetime | None = None
    quantity: int


class AssignmentCreate(BaseModel):
    model_config = ConfigDict()
    user_id: int
    start_at: datetime
    end_at: datetime
    role_id: int | None = None

    @field_validator("start_at", "end_at", mode="before")
    @classmethod
    def _ensure_tz(cls, v: datetime | str) -> datetime:
        if isinstance(v, str):
            v = datetime.fromisoformat(v)
        return _norm_dt(v)

    @field_validator("end_at")
    @classmethod
    def _end_after_start(cls, v: datetime, info):
        start = info.data.get("start_at")
        if isinstance(start, datetime) and v <= start:
            raise ValueError("end_at doit etre > start_at")
        return v


class AssignmentOut(BaseModel):
    model_config = ConfigDict(strict=True, from_attributes=True)
    id: int
    mission_id: int
    user_id: int
    role_id: int | None = None
    start_at: datetime
    end_at: datetime

