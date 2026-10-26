"""
Role-based access control on /api/v1 (issue #114).

Callers: admin, user and readonly accounts tracking ``alice_ha``, a user
account with no tracked person, the legacy bearer token, and nobody.
"""

import pytest

from api.models import User
from services.user_manager import hash_password

XHR = {"X-Requested-With": "XMLHttpRequest"}
PW = "a-test-password-123"
BEARER = {"Authorization": "Bearer legacy-token"}
_PW_HASH = hash_password(PW)  # bcrypt is slow; hash once for all fixtures


@pytest.fixture
def accounts(session_factory):
    s = session_factory()
    s.add_all(
        [
            User(username="admin", password_hash=_PW_HASH, role="admin"),
            User(
                username="alice",
                password_hash=_PW_HASH,
                role="user",
                tracked_person="alice_ha",
            ),
            User(
                username="viewer",
                password_hash=_PW_HASH,
                role="readonly",
                tracked_person="alice_ha",
            ),
            User(username="untracked", password_hash=_PW_HASH, role="user"),
        ]
    )
    s.commit()
    s.close()


def client_for(app, who):
    """A test client logged in as ``who``, or carrying the bearer token."""
    c = app.test_client()
    if who in ("admin", "alice", "viewer", "untracked"):
        r = c.post("/auth/login", json={"username": who, "password": PW}, headers=XHR)
        assert r.status_code == 200
    return c


def call(c, who, method, path, json=None):
    headers = dict(XHR)
    if who == "bearer":
        headers.update(BEARER)
    if who == "bad-bearer":
        headers["Authorization"] = "Bearer wrong"
    return c.open(path, method=method, headers=headers, json=json)


# (method, path for own data, path for someone else's data, body)
ENDPOINTS = {
    "gps-data": ("GET", "/api/v1/gps-data?user=alice_ha", "/api/v1/gps-data?user=bob_ha", None),
    "devices": ("GET", "/api/v1/users/alice_ha/devices", "/api/v1/users/bob_ha/devices", None),
    "stats": ("GET", "/api/v1/users/alice_ha/stats", "/api/v1/users/bob_ha/stats", None),
    "consent-read": (
        "GET",
        "/api/v1/users/alice_ha/consent",
        "/api/v1/users/bob_ha/consent",
        None,
    ),
    "consent-write": (
        "POST",
        "/api/v1/users/alice_ha/consent",
        "/api/v1/users/bob_ha/consent",
        {"consent": True},
    ),
    "export": ("GET", "/api/v1/users/alice_ha/export", "/api/v1/users/bob_ha/export", None),
    "delete": ("DELETE", "/api/v1/users/alice_ha/data", "/api/v1/users/bob_ha/data", None),
}

READ = ("gps-data", "devices", "stats", "consent-read")
WRITE = ("consent-write", "export", "delete")

# Expected status for (caller, endpoint) on own data / other's data.
EXPECTED = {}
for ep in ENDPOINTS:
    for who in ("admin", "bearer"):
        EXPECTED[(who, ep)] = (200, 200)
    EXPECTED[("alice", ep)] = (200, 403)
    EXPECTED[("viewer", ep)] = (200, 403) if ep in READ else (403, 403)
    EXPECTED[("untracked", ep)] = (403, 403)
    EXPECTED[("anonymous", ep)] = (401, 401)
    EXPECTED[("bad-bearer", ep)] = (401, 401)


@pytest.mark.parametrize("who,endpoint", sorted(EXPECTED))
def test_access_matrix(api_app, accounts, who, endpoint):
    method, own_path, other_path, body = ENDPOINTS[endpoint]
    want_own, want_other = EXPECTED[(who, endpoint)]
    c = client_for(api_app, who)
    assert call(c, who, method, own_path, body).status_code == want_own
    c = client_for(api_app, who)
    assert call(c, who, method, other_path, body).status_code == want_other


@pytest.mark.parametrize(
    "who,status",
    [
        ("admin", 200),
        ("bearer", 200),
        ("alice", 403),
        ("viewer", 403),
        ("anonymous", 401),
        ("bad-bearer", 401),
    ],
)
def test_user_list_is_admin_only(api_app, accounts, who, status):
    c = client_for(api_app, who)
    assert call(c, who, "GET", "/api/v1/users").status_code == status


def test_gps_data_without_user_param_forbidden_for_non_admin(api_app, accounts):
    c = client_for(api_app, "alice")
    assert c.get("/api/v1/gps-data").status_code == 403


def test_session_state_change_requires_xhr_header(api_app, accounts):
    c = client_for(api_app, "alice")
    r = c.post("/api/v1/users/alice_ha/consent", json={"consent": True})
    assert r.status_code == 403
    assert call(c, "alice", "POST", "/api/v1/users/alice_ha/consent", {"consent": True}).status_code == 200


def test_bearer_clients_need_no_xhr_header(api_app, accounts):
    c = api_app.test_client()
    r = c.delete("/api/v1/users/alice_ha/data", headers=BEARER)
    assert r.status_code == 200


def test_session_wins_over_bearer(api_app, accounts):
    """Cookie is checked first: a readonly session + valid bearer stays readonly."""
    c = client_for(api_app, "viewer")
    r = c.delete("/api/v1/users/alice_ha/data", headers={**XHR, **BEARER})
    assert r.status_code == 403


def test_bearer_disabled_when_token_unset(api_app, accounts, monkeypatch):
    import api.auth

    monkeypatch.setattr(api.auth, "BEARER_TOKEN", None)
    c = api_app.test_client()
    assert c.get("/api/v1/users", headers=BEARER).status_code == 401


def test_bearer_use_is_logged(api_app, accounts, caplog):
    c = api_app.test_client()
    with caplog.at_level("INFO", logger="api.auth"):
        c.get("/api/v1/users", headers=BEARER)
    assert "Legacy bearer-token auth used for GET /api/v1/users" in caplog.text


def test_deactivated_user_loses_api_access(api_app, accounts, session_factory):
    c = client_for(api_app, "alice")
    assert c.get("/api/v1/users/alice_ha/devices").status_code == 200
    s = session_factory()
    s.query(User).filter_by(username="alice").update({"is_active": False})
    s.commit()
    assert c.get("/api/v1/users/alice_ha/devices").status_code == 401
