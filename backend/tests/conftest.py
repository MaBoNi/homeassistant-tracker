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


@pytest.fixture
def auth_app(session_factory, monkeypatch):
    """
    Minimal Flask app with only the /auth blueprint, wired to the SQLite
    session factory. app.py itself isn't imported: it connects to Postgres
    and starts the scheduler at import time.
    """
    from flask import Flask

    import api.auth
    import api.auth_routes
    from extensions import limiter

    monkeypatch.setattr(api.auth, "Session", session_factory)
    monkeypatch.setattr(api.auth_routes, "Session", session_factory)

    app = Flask(__name__)
    app.config.update(
        TESTING=True,
        SECRET_KEY="test-secret",
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=False,
    )
    app.register_blueprint(api.auth_routes.auth_bp, url_prefix="/auth")
    limiter.init_app(app)
    limiter.reset()
    return app


@pytest.fixture
def client(auth_app):
    return auth_app.test_client()


@pytest.fixture
def api_app(auth_app, session_factory, monkeypatch):
    """
    ``auth_app`` plus the /api/v1 blueprint. GDPR routes use the SQLite
    session; the GPS query helpers in routes.py are stubbed so these tests
    exercise access control, not the Postgres-specific data layer.
    """
    import api.gdpr
    import api.geofence
    import api.routes
    from api import api_bp

    monkeypatch.setattr(api.gdpr, "Session", session_factory)
    monkeypatch.setattr(api.geofence, "Session", session_factory)
    monkeypatch.setattr(api.routes, "get_gps_logs", lambda user, *a, **kw: [{"user": user}])
    monkeypatch.setattr(api.routes, "get_unique_users", lambda: ["alice_ha", "bob_ha"])
    monkeypatch.setattr(api.routes, "get_devices_for_user", lambda u: [f"{u}-phone"])
    monkeypatch.setattr(api.routes, "get_user_stats", lambda u, **kw: {"user": u})
    monkeypatch.setattr(api.auth, "BEARER_TOKEN", "legacy-token")

    auth_app.register_blueprint(api_bp, url_prefix="/api/v1")
    return auth_app
