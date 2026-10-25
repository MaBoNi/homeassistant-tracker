# backend/api/models.py
"""
Database models for Home Assistant Tracker.
"""

from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Boolean,
    CheckConstraint,
)
from config.db import Base

USER_ROLES = ("admin", "user", "readonly")


class User(Base):
    """
    A login account (issue #112). Distinct from the Home Assistant person
    names that key ``GPSLog.user``: ``tracked_person`` links an account to the
    person whose data it may see, so role checks (#114) can enforce "own data".
    """

    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint(
            f"role IN ({', '.join(repr(r) for r in USER_ROLES)})", name="ck_users_role"
        ),
    )

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False, default="user")
    tracked_person = Column(String, nullable=True)
    created_at = Column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )
    last_login_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)

    def to_dict(self) -> dict:
        """Public representation; never includes the password hash."""
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role,
            "tracked_person": self.tracked_person,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_login_at": (
                self.last_login_at.isoformat() if self.last_login_at else None
            ),
            "is_active": bool(self.is_active),
        }

    def __repr__(self) -> str:
        return f"<User username={self.username} role={self.role}>"


class UserConsent(Base):
    """
    Tracks GDPR consent (issue #75) for a username. Users are env-driven via
    HA_USERS, so we don't have a real user table; we key consent records by
    username alone. ``consent_given_at`` is NULL until the user explicitly
    opts in.
    """

    __tablename__ = "user_consent"

    username = Column(String, primary_key=True)
    consent_given_at = Column(DateTime, nullable=True)
    consent_withdrawn_at = Column(DateTime, nullable=True)
    policy_version = Column(String, nullable=True)
    has_consent = Column(Boolean, nullable=False, default=False)

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "has_consent": bool(self.has_consent),
            "consent_given_at": (
                self.consent_given_at.isoformat() if self.consent_given_at else None
            ),
            "consent_withdrawn_at": (
                self.consent_withdrawn_at.isoformat()
                if self.consent_withdrawn_at
                else None
            ),
            "policy_version": self.policy_version,
        }


class GPSLog(Base):
    """
    Represents a GPS log entry stored in the database.
    Tracks user movement with timestamps and accuracy details.
    """

    __tablename__ = "gps_logs"

    id = Column(Integer, primary_key=True)
    user = Column(String, nullable=False)
    device = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    accuracy = Column(Float, nullable=True)

    def to_dict(self) -> dict:
        """
        Convert the GPS log entry to a dictionary format.

        Returns:
            dict: A dictionary representation of the GPS log entry.
        """
        return {
            "user": self.user,
            "device": self.device,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "timestamp": self.timestamp.isoformat(),
            "accuracy": self.accuracy,
        }

    def __repr__(self) -> str:
        """
        String representation of the GPSLog object.

        Returns:
            str: Readable representation of the GPS log entry.
        """
        return (
            f"<GPSLog user={self.user} device={self.device} timestamp={self.timestamp}>"
        )
