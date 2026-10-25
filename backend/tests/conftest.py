"""
Shared pytest fixtures. Tests run against an in-memory SQLite database so no
Postgres is needed.
"""

import os
import sys

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config.db import Base  # noqa: E402
import api.models  # noqa: E402,F401  pylint: disable=unused-import  (registers tables on Base.metadata)


@pytest.fixture
def session_factory():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    yield sessionmaker(bind=engine)
    engine.dispose()
