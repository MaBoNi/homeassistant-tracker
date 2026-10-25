# backend/services/user_manager.py

"""
Password hashing and user-account helpers (issue #112).
"""

import logging
import os

import bcrypt
from sqlalchemy.orm import sessionmaker

from api.models import User
from config.db import engine

logger = logging.getLogger(__name__)

Session = sessionmaker(bind=engine)

# bcrypt only looks at the first 72 bytes; refuse longer input rather than
# silently truncating it.
MAX_PASSWORD_BYTES = 72
ADMIN_MIN_CHARS = 12


def hash_password(plain: str) -> str:
    """
    Hash a plaintext password with bcrypt.

    Raises:
        ValueError: if the password is empty or longer than 72 bytes.
    """
    encoded = plain.encode("utf-8")
    if not encoded:
        raise ValueError("Password must not be empty")
    if len(encoded) > MAX_PASSWORD_BYTES:
        raise ValueError(f"Password must be at most {MAX_PASSWORD_BYTES} bytes")
    return bcrypt.hashpw(encoded, bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, password_hash: str) -> bool:
    """
    Check a plaintext password against a bcrypt hash (constant-time inside
    bcrypt). Returns False instead of raising on malformed or oversized input.
    """
    encoded = plain.encode("utf-8")
    if not encoded or len(encoded) > MAX_PASSWORD_BYTES or not password_hash:
        return False
    try:
        return bcrypt.checkpw(encoded, password_hash.encode("utf-8"))
    except ValueError:
        return False


def seed_initial_admin(session_factory=Session) -> bool:
    """
    Create an admin from INITIAL_ADMIN_USERNAME / INITIAL_ADMIN_PASSWORD if
    the users table is empty. Safe to call on every startup.

    Returns:
        bool: True if an admin was created.
    """
    s = session_factory()
    try:
        if s.query(User).first() is not None:
            return False

        username = os.getenv("INITIAL_ADMIN_USERNAME", "").strip()
        password = os.getenv("INITIAL_ADMIN_PASSWORD", "")
        if not username or not password:
            logger.warning(
                "No users exist and INITIAL_ADMIN_USERNAME / INITIAL_ADMIN_PASSWORD "
                "are not set; no admin account was created."
            )
            return False
        if len(password) < ADMIN_MIN_CHARS:
            logger.error(
                "INITIAL_ADMIN_PASSWORD must be at least %d characters; "
                "no admin account was created.",
                ADMIN_MIN_CHARS,
            )
            return False

        s.add(User(username=username, password_hash=hash_password(password), role="admin"))
        s.commit()
        logger.info("Seeded initial admin account '%s'.", username)
        return True
    except Exception:
        s.rollback()
        logger.exception("Failed to seed initial admin account.")
        return False
    finally:
        s.close()
