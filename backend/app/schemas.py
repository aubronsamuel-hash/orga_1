import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator, ConfigDict

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
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None


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
    totp_code: Optional[str] = None


# --- Missions (J4) ---

class MissionBase(BaseModel):
    model_config = ConfigDict(strict=True)
    title: str = Field(min_length=2)
    location: Optional[str] = None
    start_at: datetime
    end_at: datetime
    description: Optional[str] = None

    @field_validator("end_at")
    @classmethod
    def _end_after_start(cls, v: datetime, info):
        start = info.data.get("start_at")
        if isinstance(start, datetime) and v <= start:
            raise ValueError("end_at doit etre > start_at")
        return v


class MissionCreate(MissionBase):
    pass


class MissionUpdate(BaseModel):
    model_config = ConfigDict(strict=True)
    title: Optional[str] = None
    location: Optional[str] = None
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    description: Optional[str] = None

    @field_validator("end_at")
    @classmethod
    def _end_after_start(cls, v: Optional[datetime], info):
        start = info.data.get("start_at")
        if v is not None and start is not None and v <= start:
            raise ValueError("end_at doit etre > start_at")
        return v


class MissionOut(MissionBase):
    model_config = ConfigDict(strict=True, from_attributes=True)
    id: int


class MissionDetail(MissionOut):
    roles: list["MissionRoleOut"] = []
    assignments: list["AssignmentOut"] = []


class MissionRoleCreate(BaseModel):
    model_config = ConfigDict(strict=True)
    name: str = Field(min_length=2)
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    quantity: int = Field(default=1, ge=1)


class MissionRoleUpdate(BaseModel):
    model_config = ConfigDict(strict=True)
    name: Optional[str] = None
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    quantity: Optional[int] = Field(default=None, ge=1)


class MissionRoleOut(BaseModel):
    model_config = ConfigDict(strict=True, from_attributes=True)
    id: int
    mission_id: int
    name: str
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    quantity: int


class AssignmentCreate(BaseModel):
    model_config = ConfigDict(strict=True)
    user_id: int
    start_at: datetime
    end_at: datetime
    role_id: Optional[int] = None

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
    role_id: Optional[int] = None
    start_at: datetime
    end_at: datetime

