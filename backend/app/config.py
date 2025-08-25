from functools import lru_cache
from pydantic import BaseModel
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


class Health(BaseModel):
    status: str
    time_utc: str


class Version(BaseModel):
    version: str
    git_sha: str


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()  # type: ignore[arg-type]

