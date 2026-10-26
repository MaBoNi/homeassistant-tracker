# backend/api/auth_routes.py
"""
Session-cookie authentication endpoints (issue #113), mounted at ``/auth``.

The session is Flask's itsdangerous-signed cookie holding only ``user_id``;
no server-side store. CSRF is mitigated by ``SameSite=Lax`` plus a required
``X-Requested-With`` header on every state-changing request, which a
cross-site form post cannot set.
"""

import logging
import re
from datetime import datetime, timezone

from flask import Blueprint, jsonify, request, session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from api.models import LoginEvent, User, USER_ROLES
from config.db import engine
from extensions import limiter
from services.user_manager import (
    MAX_PASSWORD_BYTES,
    hash_password,
    verify_password,
)
from .auth import get_current_user

logger = logging.getLogger(__name__)

auth_bp = Blueprint("auth", __name__)

Session = sessionmaker(bind=engine)

USERNAME_RE = re.compile(r"^[A-Za-z0-9_.-]{1,64}$")
PASSWORD_MIN_CHARS = 12
UA_MAX_LEN = 512

# Hash of a throwaway value, checked when the username is unknown so a failed
# login takes about as long whether or not the account exists.
_DUMMY_HASH = hash_password("timing-equaliser-not-a-real-password")


@auth_bp.before_request
def _require_xhr_header():
    if request.method in ("POST", "PUT", "PATCH", "DELETE"):
        if request.headers.get("X-Requested-With") != "XMLHttpRequest":
            return jsonify({"message": "Missing X-Requested-With header"}), 403
    return None


def _json_body():
    data = request.get_json(silent=True)
    return data if isinstance(data, dict) else {}


def _record_login(s, user_id, username, success):
    ua = request.headers.get("User-Agent")
    s.add(
        LoginEvent(
            user_id=user_id,
            username=username[:64] if username else None,
            ip=request.remote_addr,
            ua=ua[:UA_MAX_LEN] if ua else None,
            success=success,
        )
    )


@auth_bp.route("/login", methods=["POST"])
@limiter.limit("5 per minute", deduct_when=lambda response: response.status_code == 401)
def login():
    """
    Body: ``{ "username": str, "password": str }``. On success sets the
    session cookie and returns the user; 401 with a generic message otherwise.
    Only failed attempts count towards the 5/minute limit.
    """
    data = _json_body()
    username = data.get("username")
    password = data.get("password")
    if not isinstance(username, str) or not isinstance(password, str):
        return jsonify({"message": "username and password are required"}), 400

    s = Session()
    try:
        user = s.query(User).filter_by(username=username).first()
        if user is None:
            verify_password(password, _DUMMY_HASH)
            ok = False
        else:
            ok = verify_password(password, user.password_hash) and bool(user.is_active)

        _record_login(s, user.id if user else None, username, ok)
        if not ok:
            s.commit()
            logger.warning(f"Failed login from {request.remote_addr}")
            return jsonify({"message": "Invalid username or password"}), 401

        user.last_login_at = datetime.now(timezone.utc)
        s.commit()

        # Fresh cookie on login so a pre-existing session value can't carry over.
        session.clear()
        session["user_id"] = user.id
        session.permanent = True
        logger.info(f"User {user.username} logged in from {request.remote_addr}")
        return jsonify(_public_user(user)), 200
    finally:
        s.close()


@auth_bp.route("/logout", methods=["POST"])
def logout():
    """Clear the session cookie. Always succeeds."""
    session.clear()
    return jsonify({"message": "Logged out"}), 200


@auth_bp.route("/me", methods=["GET"])
def me():
    """Return the logged-in user, or 401."""
    user = get_current_user()
    if user is None:
        return jsonify({"message": "Authentication is required"}), 401
    return jsonify(_public_user(user)), 200


@auth_bp.route("/register", methods=["POST"])
@limiter.limit("20 per hour")
def register():
    """
    Admin-only. Body: ``{ username, password, role?, tracked_person? }``.
    Returns 201 with the new user. The first admin comes from
    INITIAL_ADMIN_USERNAME / INITIAL_ADMIN_PASSWORD, not from this endpoint.
    """
    current, error = _admin_or_error()
    if error:
        return error

    data = _json_body()
    error = _registration_error(data)
    if error:
        return jsonify({"message": error}), 400
    username = data["username"]
    password = data["password"]
    role = data.get("role", "user")
    tracked_person = data.get("tracked_person")

    s = Session()
    try:
        user = User(
            username=username,
            password_hash=hash_password(password),
            role=role,
            tracked_person=tracked_person or None,
        )
        s.add(user)
        s.commit()
        logger.info(f"Admin {current.username} registered user {username} ({role})")
        return jsonify(user.to_dict()), 201
    except IntegrityError:
        s.rollback()
        return jsonify({"message": "username already exists"}), 409
    finally:
        s.close()


def _admin_or_error():
    """Return ``(admin_user, None)`` or ``(None, error_response)``."""
    current = get_current_user()
    if current is None:
        return None, (jsonify({"message": "Authentication is required"}), 401)
    if current.role != "admin":
        return None, (jsonify({"message": "Admin role required"}), 403)
    return current, None


@auth_bp.route("/users", methods=["GET"])
def list_users():
    """Admin-only list of login accounts (issue #115 admin panel)."""
    _, error = _admin_or_error()
    if error:
        return error
    s = Session()
    try:
        return jsonify([u.to_dict() for u in s.query(User).order_by(User.username)]), 200
    finally:
        s.close()


@auth_bp.route("/users/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    """
    Admin-only. Body may contain ``role``, ``is_active`` and ``tracked_person``
    (empty string or null clears it). Admins cannot demote or deactivate
    themselves, so the last admin can't lock everyone out by accident.
    """
    current, error = _admin_or_error()
    if error:
        return error

    changes, message = _user_changes(_json_body())
    if not message and user_id == current.id and (
        changes.get("role", "admin") != "admin" or changes.get("is_active") is False
    ):
        message = "You cannot demote or deactivate your own account"
    if message:
        return jsonify({"message": message}), 400

    s = Session()
    try:
        user = s.get(User, user_id)
        if user is None:
            return jsonify({"message": "User not found"}), 404
        for field, value in changes.items():
            setattr(user, field, value)
        s.commit()
        logger.info(f"Admin {current.username} updated user {user.username}: {sorted(changes)}")
        return jsonify(user.to_dict()), 200
    finally:
        s.close()


def _user_changes(data):
    """Validate a PATCH /users body. Returns ``(changes, error_message)``."""
    changes = {}
    if "role" in data:
        if data["role"] not in USER_ROLES:
            return {}, f"role must be one of {', '.join(USER_ROLES)}"
        changes["role"] = data["role"]
    if "is_active" in data:
        if not isinstance(data["is_active"], bool):
            return {}, "is_active must be true or false"
        changes["is_active"] = data["is_active"]
    if "tracked_person" in data:
        if data["tracked_person"] is not None and not isinstance(data["tracked_person"], str):
            return {}, "tracked_person must be a string"
        changes["tracked_person"] = data["tracked_person"] or None
    if not changes:
        return {}, "Nothing to update"
    return changes, None


def _registration_error(data):
    """Return a validation message for a /register body, or None if valid."""
    username = data.get("username")
    password = data.get("password")
    tracked_person = data.get("tracked_person")
    if not isinstance(username, str) or not USERNAME_RE.match(username):
        return "username must be 1-64 chars of A-Z a-z 0-9 _ . -"
    if (
        not isinstance(password, str)
        or len(password) < PASSWORD_MIN_CHARS
        or len(password.encode("utf-8")) > MAX_PASSWORD_BYTES
    ):
        return (
            f"password must be {PASSWORD_MIN_CHARS}+ characters "
            f"and at most {MAX_PASSWORD_BYTES} bytes"
        )
    if data.get("role", "user") not in USER_ROLES:
        return f"role must be one of {', '.join(USER_ROLES)}"
    if tracked_person is not None and not isinstance(tracked_person, str):
        return "tracked_person must be a string"
    return None


def _public_user(user):
    return {
        "id": user.id,
        "username": user.username,
        "role": user.role,
        "tracked_person": user.tracked_person,
    }
