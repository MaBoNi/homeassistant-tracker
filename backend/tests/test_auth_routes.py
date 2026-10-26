import pytest

from api.models import LoginEvent, User
from services.user_manager import hash_password

XHR = {"X-Requested-With": "XMLHttpRequest"}
ADMIN_PW = "admin-password-123"
USER_PW = "user-password-1234"


@pytest.fixture
def users(session_factory):
    s = session_factory()
    s.add_all(
        [
            User(username="admin", password_hash=hash_password(ADMIN_PW), role="admin"),
            User(
                username="alice",
                password_hash=hash_password(USER_PW),
                role="user",
                tracked_person="alice_ha",
            ),
            User(
                username="ghost",
                password_hash=hash_password(USER_PW),
                is_active=False,
            ),
        ]
    )
    s.commit()
    s.close()


def login(client, username, password, headers=XHR):
    return client.post(
        "/auth/login", json={"username": username, "password": password}, headers=headers
    )


class TestLogin:
    def test_success_sets_httponly_lax_cookie(self, client, users, session_factory):
        r = login(client, "alice", USER_PW)
        assert r.status_code == 200
        assert r.get_json() == {
            "id": 2,
            "username": "alice",
            "role": "user",
            "tracked_person": "alice_ha",
        }
        cookie = r.headers["Set-Cookie"]
        assert "HttpOnly" in cookie
        assert "SameSite=Lax" in cookie
        u = session_factory().query(User).filter_by(username="alice").one()
        assert u.last_login_at is not None

    def test_wrong_password(self, client, users):
        r = login(client, "alice", "nope-nope-nope")
        assert r.status_code == 401
        assert r.get_json()["message"] == "Invalid username or password"
        assert "Set-Cookie" not in r.headers

    def test_unknown_user_same_message(self, client, users):
        r = login(client, "nobody", "whatever-password")
        assert r.status_code == 401
        assert r.get_json()["message"] == "Invalid username or password"

    def test_inactive_user_rejected(self, client, users):
        assert login(client, "ghost", USER_PW).status_code == 401

    def test_missing_fields(self, client, users):
        assert client.post("/auth/login", json={}, headers=XHR).status_code == 400
        assert client.post("/auth/login", data="x", headers=XHR).status_code == 400

    def test_requires_xhr_header(self, client, users):
        assert login(client, "alice", USER_PW, headers={}).status_code == 403

    def test_login_events_recorded(self, client, users, session_factory):
        login(client, "alice", "wrong-password-x")
        login(client, "nobody", "wrong-password-x")
        client.post(
            "/auth/login",
            json={"username": "alice", "password": USER_PW},
            headers={**XHR, "User-Agent": "pytest-ua"},
        )
        events = session_factory().query(LoginEvent).order_by(LoginEvent.id).all()
        assert [(e.user_id, e.username, e.success) for e in events] == [
            (2, "alice", False),
            (None, "nobody", False),
            (2, "alice", True),
        ]
        assert events[-1].ua == "pytest-ua"
        assert events[-1].ip == "127.0.0.1"
        assert all(e.ts is not None for e in events)

    def test_failed_logins_rate_limited(self, client, users):
        for _ in range(5):
            assert login(client, "alice", "wrong-password-x").status_code == 401
        assert login(client, "alice", "wrong-password-x").status_code == 429
        assert login(client, "alice", USER_PW).status_code == 429

    def test_successful_logins_not_counted(self, client, users):
        for _ in range(8):
            assert login(client, "alice", USER_PW).status_code == 200


class TestMeAndLogout:
    def test_me_requires_login(self, client, users):
        assert client.get("/auth/me").status_code == 401

    def test_full_flow(self, client, users):
        login(client, "alice", USER_PW)
        r = client.get("/auth/me")
        assert r.status_code == 200
        assert r.get_json()["username"] == "alice"
        assert client.post("/auth/logout", headers=XHR).status_code == 200
        assert client.get("/auth/me").status_code == 401

    def test_logout_requires_xhr_header(self, client, users):
        login(client, "alice", USER_PW)
        assert client.post("/auth/logout").status_code == 403
        assert client.get("/auth/me").status_code == 200

    def test_deactivated_user_session_dropped(self, client, users, session_factory):
        login(client, "alice", USER_PW)
        s = session_factory()
        s.query(User).filter_by(username="alice").update({"is_active": False})
        s.commit()
        assert client.get("/auth/me").status_code == 401

    def test_forged_cookie_rejected(self, auth_app, users):
        c = auth_app.test_client()
        c.set_cookie("session", "eyJ1c2VyX2lkIjoxfQ.forged.signature")
        assert c.get("/auth/me").status_code == 401


class TestRegister:
    def body(self, **kw):
        return {"username": "bob", "password": "bob-password-123", **kw}

    def test_requires_login(self, client, users):
        r = client.post("/auth/register", json=self.body(), headers=XHR)
        assert r.status_code == 401

    def test_requires_admin(self, client, users):
        login(client, "alice", USER_PW)
        r = client.post("/auth/register", json=self.body(), headers=XHR)
        assert r.status_code == 403

    def test_admin_creates_user_who_can_log_in(self, client, users, auth_app):
        login(client, "admin", ADMIN_PW)
        r = client.post(
            "/auth/register",
            json=self.body(role="readonly", tracked_person="bob_ha"),
            headers=XHR,
        )
        assert r.status_code == 201
        body = r.get_json()
        assert body["username"] == "bob"
        assert body["role"] == "readonly"
        assert body["tracked_person"] == "bob_ha"
        assert "password_hash" not in body

        other = auth_app.test_client()
        assert login(other, "bob", "bob-password-123").status_code == 200

    def test_defaults_to_user_role(self, client, users):
        login(client, "admin", ADMIN_PW)
        r = client.post("/auth/register", json=self.body(), headers=XHR)
        assert r.get_json()["role"] == "user"

    def test_duplicate_username(self, client, users):
        login(client, "admin", ADMIN_PW)
        r = client.post("/auth/register", json=self.body(username="alice"), headers=XHR)
        assert r.status_code == 409

    @pytest.mark.parametrize(
        "override",
        [
            {"username": ""},
            {"username": "has space"},
            {"username": "x" * 65},
            {"password": "short"},
            {"password": "a" * 73},
            {"role": "superuser"},
            {"tracked_person": 42},
        ],
    )
    def test_validation(self, client, users, override):
        login(client, "admin", ADMIN_PW)
        r = client.post("/auth/register", json=self.body(**override), headers=XHR)
        assert r.status_code == 400

    def test_requires_xhr_header(self, client, users):
        login(client, "admin", ADMIN_PW)
        assert client.post("/auth/register", json=self.body()).status_code == 403
