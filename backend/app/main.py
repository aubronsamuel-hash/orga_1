from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1.auth import router as auth_router
from .api.v1.missions import router as missions_router
from .api.v1.router import router as v1_meta_router
from .api.v1.users import router as users_router
from .config import get_settings
from .errors import install_error_handlers
from .logging_utils import setup_logging
from .middleware import RequestIdMiddleware


def create_app() -> FastAPI:
    s = get_settings()
    setup_logging(s.log_level)

    app = FastAPI(
        title=s.app_name,
        version=s.api_version,
        openapi_url="/api/v1/openapi.json",
        debug=True,
    )

    app.add_middleware(RequestIdMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    install_error_handlers(app)
    app.include_router(v1_meta_router, prefix="/api/v1")
    app.include_router(auth_router, prefix="/api/v1")
    app.include_router(users_router, prefix="/api/v1")
    app.include_router(missions_router, prefix="/api/v1")

    return app


app = create_app()
