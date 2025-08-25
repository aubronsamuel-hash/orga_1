from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .errors import install_error_handlers
from .logging_utils import setup_logging
from .middleware import RequestIdMiddleware
from .api.v1.router import router as v1_router


def create_app() -> FastAPI:
    s = get_settings()
    setup_logging(s.log_level)

    app = FastAPI(title=s.app_name, version=s.api_version, openapi_url="/api/v1/openapi.json")

    app.add_middleware(RequestIdMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    install_error_handlers(app)
    app.include_router(v1_router, prefix="/api/v1")
    return app


app = create_app()

