from functools import lru_cache
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict  # type: ignore


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Coulisses Crew"
    app_env: str = "dev"
    api_version: str = "0.1.0"
    git_sha: str = "dev"

    api_host: str = "127.0.0.1"
    api_port: int = 8000
    log_level: str = "INFO"
    request_id_header: str = "X-Request-ID"
    tz: str = "UTC"

    database_url: str = "sqlite:///dev.db"

    jwt_secret: str = "change-me-in-dev"
    jwt_alg: str = "HS256"
    access_ttl_seconds: int = 900
    refresh_ttl_seconds: int = 60 * 60 * 24 * 14

    bcrypt_rounds: int = 12

    rate_limit_login_max: int = 5
    rate_limit_login_window_sec: int = 60
    auth_max_fails: int = 5
    auth_lock_minutes: int = 10

    redis_url: str | None = None


class Health(BaseModel):
    status: str
    time_utc: str


class Version(BaseModel):
    version: str
    git_sha: str


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()  # type: ignore[arg-type]

