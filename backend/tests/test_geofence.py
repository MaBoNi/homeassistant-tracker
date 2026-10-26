"""Geofence zone CRUD (issue #116)."""

import pytest

from api.models import GeofenceZone, User
from services.user_manager import hash_password

XHR = {"X-Requested-With": "XMLHttpRequest"}
BEARER = {"Authorization": "Bearer legacy-token", "X-Requested-With": "XMLHttpRequest"}
PW = "a-test-password-123"
_PW_HASH = hash_password(PW)  # bcrypt is slow; hash once
ZONES = "/api/v1/users/alice_ha/zones"
HOME = {"name": "Home", "center_lat": 55.6761, "center_lon": 12.5683, "radius_m": 150}


@pytest.fixture
def accounts(session_factory):
    s = session_factory()
    s.add_all(
        [
            User(username="alice", password_hash=_PW_HASH, role="user", tracked_person="alice_ha"),
            User(username="viewer", password_hash=_PW_HASH, role="readonly", tracked_person="alice_ha"),
            User(username="bob", password_hash=_PW_HASH, role="user", tracked_person="bob_ha"),
        ]
    )
    s.commit()
    s.close()


def as_user(app, username):
    c = app.test_client()
    r = c.post("/auth/login", json={"username": username, "password": PW}, headers=XHR)
    assert r.status_code == 200
    return c


@pytest.fixture
def alice(api_app, accounts):
    return as_user(api_app, "alice")


def create(c, **overrides):
    return c.post(ZONES, json={**HOME, **overrides}, headers=XHR)


class TestCreateAndList:
    def test_create_then_list(self, alice):
        r = create(alice)
        assert r.status_code == 201
        zone = r.get_json()
        assert zone["owner_user"] == "alice_ha"
        assert zone["geometry_type"] == "circle"
        assert zone["active"] is True
        assert zone["radius_m"] == 150.0
        assert zone["created_at"]

        r = alice.get(ZONES)
        assert r.status_code == 200
        assert [z["name"] for z in r.get_json()] == ["Home"]

    def test_list_empty(self, alice):
        assert alice.get(ZONES).get_json() == []

    def test_create_inactive_and_name_trimmed(self, alice):
        zone = create(alice, name="  Work  ", active=False).get_json()
        assert zone["name"] == "Work"
        assert zone["active"] is False

    def test_lists_only_own_zones(self, api_app, accounts, session_factory):
        s = session_factory()
        s.add(GeofenceZone(owner_user="bob_ha", name="Bob home", center_lat=1, center_lon=1, radius_m=100))
        s.commit()
        alice = as_user(api_app, "alice")
        create(alice)
        assert [z["name"] for z in alice.get(ZONES).get_json()] == ["Home"]

    @pytest.mark.parametrize(
        "override",
        [
            {"name": ""},
            {"name": "   "},
            {"name": "x" * 101},
            {"name": 5},
            {"center_lat": 90.1},
            {"center_lat": -90.1},
            {"center_lat": "55"},
            {"center_lat": True},
            {"center_lon": 180.5},
            {"center_lon": None},
            {"radius_m": 9.9},
            {"radius_m": 50001},
            {"radius_m": "100"},
            {"active": "yes"},
        ],
    )
    def test_validation(self, alice, override):
        assert create(alice, **override).status_code == 400

    @pytest.mark.parametrize(
        "override",
        [{"radius_m": 10}, {"radius_m": 50000}, {"center_lat": -90, "center_lon": 180}],
    )
    def test_boundaries_accepted(self, alice, override):
        assert create(alice, **override).status_code == 201

    def test_missing_body(self, alice):
        assert alice.post(ZONES, headers=XHR).status_code == 400

    def test_limit_50_per_user(self, alice, session_factory):
        s = session_factory()
        s.add_all(
            [
                GeofenceZone(owner_user="alice_ha", name=f"z{i}", center_lat=0, center_lon=0, radius_m=100)
                for i in range(50)
            ]
        )
        s.commit()
        r = create(alice)
        assert r.status_code == 409


class TestUpdateAndDelete:
    def test_rename_and_toggle(self, alice):
        zone_id = create(alice).get_json()["id"]
        r = alice.patch(f"{ZONES}/{zone_id}", json={"name": "Home sweet home"}, headers=XHR)
        assert r.status_code == 200
        assert r.get_json()["name"] == "Home sweet home"
        r = alice.patch(f"{ZONES}/{zone_id}", json={"active": False}, headers=XHR)
        assert r.get_json()["active"] is False
        assert r.get_json()["radius_m"] == 150.0

    @pytest.mark.parametrize("body", [{}, {"name": ""}, {"active": 1}, {"radius_m": 500}])
    def test_update_validation(self, alice, body):
        zone_id = create(alice).get_json()["id"]
        assert alice.patch(f"{ZONES}/{zone_id}", json=body, headers=XHR).status_code == 400

    def test_delete(self, alice):
        zone_id = create(alice).get_json()["id"]
        r = alice.delete(f"{ZONES}/{zone_id}", headers=XHR)
        assert r.status_code == 200
        assert r.get_json() == {"deleted": zone_id}
        assert alice.get(ZONES).get_json() == []
        assert alice.delete(f"{ZONES}/{zone_id}", headers=XHR).status_code == 404

    def test_unknown_zone(self, alice):
        assert alice.patch(f"{ZONES}/999", json={"active": False}, headers=XHR).status_code == 404
        assert alice.delete(f"{ZONES}/999", headers=XHR).status_code == 404

    def test_zone_id_under_wrong_person_is_404(self, api_app, accounts, session_factory):
        """Admin (bearer) addressing bob's zone through alice's URL must not touch it."""
        s = session_factory()
        bob_zone = GeofenceZone(owner_user="bob_ha", name="Bob", center_lat=1, center_lon=1, radius_m=100)
        s.add(bob_zone)
        s.commit()
        zid = bob_zone.id
        c = api_app.test_client()
        assert c.patch(f"{ZONES}/{zid}", json={"active": False}, headers=BEARER).status_code == 404
        assert c.delete(f"{ZONES}/{zid}", headers=BEARER).status_code == 404
        assert session_factory().get(GeofenceZone, zid).active is True


class TestAccess:
    def test_readonly_can_list_but_not_change(self, api_app, accounts, alice):
        zone_id = create(alice).get_json()["id"]
        viewer = as_user(api_app, "viewer")
        assert viewer.get(ZONES).status_code == 200
        assert create(viewer).status_code == 403
        assert viewer.patch(f"{ZONES}/{zone_id}", json={"active": False}, headers=XHR).status_code == 403
        assert viewer.delete(f"{ZONES}/{zone_id}", headers=XHR).status_code == 403

    def test_other_user_forbidden(self, api_app, accounts):
        bob = as_user(api_app, "bob")
        assert bob.get(ZONES).status_code == 403
        assert create(bob).status_code == 403

    def test_bearer_has_admin_access(self, api_app, accounts):
        c = api_app.test_client()
        assert c.post(ZONES, json=HOME, headers=BEARER).status_code == 201
        assert c.get(ZONES, headers=BEARER).status_code == 200

    def test_anonymous(self, api_app, accounts):
        c = api_app.test_client()
        assert c.get(ZONES).status_code == 401
        assert c.post(ZONES, json=HOME, headers=XHR).status_code == 401

    def test_cookie_writes_need_xhr_header(self, alice):
        assert alice.post(ZONES, json=HOME).status_code == 403
