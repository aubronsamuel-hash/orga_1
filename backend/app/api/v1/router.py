from datetime import UTC, datetime

from fastapi import APIRouter

from ...config import Health, Version, get_settings

router = APIRouter()


@router.get("/health", response_model=Health, tags=["meta"])
def health() -> Health:
    return Health(status="ok", time_utc=datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"))


@router.get("/version", response_model=Version, tags=["meta"])
def version() -> Version:
    s = get_settings()
    return Version(version=s.api_version, git_sha=s.git_sha)

