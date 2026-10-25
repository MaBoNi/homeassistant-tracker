import logging

import pytest
from sqlalchemy.exc import IntegrityError

from api.models import User
from services.user_manager import hash_password, seed_initial_admin, verify_password


class TestPasswordHashing:
    def test_round_trip(self):
        h = hash_password("correct horse battery staple")
        assert h != "correct horse battery staple"
        assert verify_password("correct horse battery staple", h)

    def test_wrong_password_rejected(self):
        assert not verify_password("wrong", hash_password("right-password"))

    def test_hashes_are_salted(self):
        assert hash_password("same-password") != hash_password("same-password")

    def test_unicode_password(self):
        assert verify_password("pæssw✓rd-ø", hash_password("pæssw✓rd-ø"))

    def test_empty_password_cannot_be_hashed(self):
        with pytest.raises(ValueError):
            hash_password("")

    def test_password_over_72_bytes_rejected(self):
        with pytest.raises(ValueError):
            hash_password("a" * 73)
        assert hash_password("a" * 72)

    def test_verify_never_raises_on_bad_input(self):
        h = hash_password("right-password")
        assert not verify_password("", h)
        assert not verify_password("a" * 100, h)
        assert not verify_password("right-password", "")
        assert not verify_password("right-password", "not-a-bcrypt-hash")


class TestUserModel:
    def test_defaults_and_to_dict_hides_hash(self, session_factory):
        s = session_factory()
        s.add(User(username="alice", password_hash=hash_password("pw-alice-123")))
        s.commit()
        u = s.query(User).one()
        assert u.role == "user"
        assert u.is_active is True
        assert u.created_at is not None
        assert u.tracked_person is None
        d = u.to_dict()
        assert "password_hash" not in d
        assert d["username"] == "alice"

    def test_username_unique(self, session_factory):
        s = session_factory()
        s.add(User(username="bob", password_hash="x"))
        s.commit()
        s.add(User(username="bob", password_hash="y"))
        with pytest.raises(IntegrityError):
            s.commit()

    def test_invalid_role_rejected(self, session_factory):
        s = session_factory()
        s.add(User(username="eve", password_hash="x", role="superuser"))
        with pytest.raises(IntegrityError):
            s.commit()


class TestSeedInitialAdmin:
    def test_seeds_admin_when_table_empty(self, session_factory, monkeypatch):
        monkeypatch.setenv("INITIAL_ADMIN_USERNAME", "root")
        monkeypatch.setenv("INITIAL_ADMIN_PASSWORD", "a-long-enough-password")
        assert seed_initial_admin(session_factory) is True
        u = session_factory().query(User).one()
        assert u.username == "root"
        assert u.role == "admin"
        assert verify_password("a-long-enough-password", u.password_hash)

    def test_idempotent(self, session_factory, monkeypatch):
        monkeypatch.setenv("INITIAL_ADMIN_USERNAME", "root")
        monkeypatch.setenv("INITIAL_ADMIN_PASSWORD", "a-long-enough-password")
        assert seed_initial_admin(session_factory) is True
        assert seed_initial_admin(session_factory) is False
        assert session_factory().query(User).count() == 1

    def test_skips_when_users_exist(self, session_factory, monkeypatch):
        s = session_factory()
        s.add(User(username="existing", password_hash="x"))
        s.commit()
        monkeypatch.setenv("INITIAL_ADMIN_USERNAME", "root")
        monkeypatch.setenv("INITIAL_ADMIN_PASSWORD", "a-long-enough-password")
        assert seed_initial_admin(session_factory) is False
        assert session_factory().query(User).count() == 1

    def test_warns_when_env_missing(self, session_factory, monkeypatch, caplog):
        monkeypatch.delenv("INITIAL_ADMIN_USERNAME", raising=False)
        monkeypatch.delenv("INITIAL_ADMIN_PASSWORD", raising=False)
        with caplog.at_level(logging.WARNING):
            assert seed_initial_admin(session_factory) is False
        assert "no admin account was created" in caplog.text
        assert session_factory().query(User).count() == 0

    def test_rejects_short_password(self, session_factory, monkeypatch):
        monkeypatch.setenv("INITIAL_ADMIN_USERNAME", "root")
        monkeypatch.setenv("INITIAL_ADMIN_PASSWORD", "short")
        assert seed_initial_admin(session_factory) is False
        assert session_factory().query(User).count() == 0
