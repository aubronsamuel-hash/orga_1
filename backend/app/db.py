from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from .config import get_settings

_engine = None
_SessionLocal = None


class Base(DeclarativeBase):
    pass


def _init_engine():
    global _engine, _SessionLocal
    s = get_settings()
    url = s.database_url
    connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
    _engine = create_engine(url, echo=False, future=True, connect_args=connect_args)
    _SessionLocal = sessionmaker(bind=_engine, autoflush=False, expire_on_commit=False, future=True)


def get_engine():
    global _engine
    if _engine is None:
        _init_engine()
    return _engine


def get_session_factory():
    global _SessionLocal
    if _SessionLocal is None:
        _init_engine()
    return _SessionLocal


@contextmanager
def session_scope() -> Iterator["Session"]:
    Session = get_session_factory()
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

