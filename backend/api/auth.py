# backend/api/auth.py
"""
Authentication and role-based access control for Flask routes.

A request is authenticated by, in order:
1. the signed session cookie from ``/auth/login`` (issue #113), resolving to
   a ``User`` with a role, or
2. the legacy ``Authorization: Bearer <TRACKER_APP_TOKEN>`` header, which is
   treated as admin so existing clients keep working (issue #110). Every use
   is logged so it can be deprecated.
"""

import os
import secrets
import logging
from functools import wraps
from flask import g, request, jsonify, session
from sqlalchemy.orm import sessionmaker

from api.models import User
from config.db import engine

# Set up logging
logger = logging.getLogger(__name__)

# Fetch the TRACKER_APP_TOKEN from the environment
BEARER_TOKEN = os.getenv("TRACKER_APP_TOKEN")

Session = sessionmaker(bind=engine)

STATE_CHANGING_METHODS = ("POST", "PUT", "PATCH", "DELETE")


def get_current_user():
    """
    Return the active ``User`` for the session cookie (issue #113), or None.
    A cookie that points at a deleted or deactivated account is cleared.
    """
    user_id = session.get("user_id")
    if user_id is None:
        return None
    s = Session()
    try:
        user = s.get(User, user_id)
        if user is None or not user.is_active:
            session.clear()
            return None
        s.expunge(user)
        return user
    finally:
        s.close()


def current_user():
    """The ``User`` authenticated for this request by ``@require_role``, or None."""
    return g.get("current_user")


def _bearer_token_valid():
    header = request.headers.get("Authorization", "")
    if not header.startswith("Bearer ") or not BEARER_TOKEN:
        return False
    # Use constant-time comparison to prevent timing attacks
    return secrets.compare_digest(header[7:], BEARER_TOKEN)


def _target_person(own_kwarg, own_query, kwargs):
    if own_kwarg:
        return kwargs.get(own_kwarg)
    if own_query:
        return request.args.get(own_query)
    return None


def require_role(*roles, own_kwarg=None, own_query=None):
    """
    Allow the request if the caller is an admin, or has one of ``roles``.

    For non-admins, ``own_kwarg`` (a URL variable) or ``own_query`` (a query
    parameter) names the Home Assistant person being accessed; it must equal
    the caller's ``User.tracked_person`` ("own data", issue #114).

    Responses: 401 when not authenticated, 403 when authenticated but not
    allowed, or when a cookie-authenticated state-changing request lacks the
    ``X-Requested-With`` CSRF header.
    """

    def session_denial(user, kwargs):
        """Return the 403 message for a cookie-authenticated user, or None if allowed."""
        if (
            request.method in STATE_CHANGING_METHODS
            and request.headers.get("X-Requested-With") != "XMLHttpRequest"
        ):
            return "Missing X-Requested-With header"
        if user.role == "admin":
            return None
        if user.role not in roles:
            return "Insufficient role"
        if own_kwarg or own_query:
            target = _target_person(own_kwarg, own_query, kwargs)
            if not user.tracked_person or target != user.tracked_person:
                return "Access to this user's data is not allowed"
        return None

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = get_current_user()
            if user is not None:
                denial = session_denial(user, kwargs)
                if denial:
                    return jsonify({"message": denial}), 403
                g.current_user = user
                g.auth_method = "session"
                return f(*args, **kwargs)

            if _bearer_token_valid():
                g.current_user = None
                g.auth_method = "bearer"
                logger.info(f"Legacy bearer-token auth used for {request.method} {request.path}")
                return f(*args, **kwargs)

            if "Authorization" in request.headers:
                logger.warning(f"Failed authentication attempt from {request.remote_addr}")
                return jsonify({"message": "Invalid authentication credentials"}), 401
            logger.warning(f"Authentication attempt without credentials from {request.remote_addr}")
            return jsonify({"message": "Authentication is required"}), 401

        return decorated_function

    return decorator
