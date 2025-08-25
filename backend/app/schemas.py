import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class UserCreate(BaseModel):
    email: str = Field(...)
    password: str = Field(min_length=8)

    @field_validator("email")
    @classmethod
    def _email(cls, v: str) -> str:
        if not EMAIL_RE.match(v):
            raise ValueError("email invalide")
        return v.lower()


class UserOut(BaseModel):
    id: int
    email: str
    is_active: bool
    is_admin: bool
    totp_enabled: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class LoginIn(BaseModel):
    email: str
    password: str
    totp_code: Optional[str] = None

