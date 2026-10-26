# backend/config/config.py

"""
Configuration settings for the Home Assistant Tracker application.
Environment variables can override the default values.
"""

import os


class Config:
    """
    Holds Flask and external service configuration loaded from environment variables.
    """

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:your_password@gps_tracker_db:5432/gps_tracker",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    HA_API_URL = os.getenv("HA_API_URL", "http://your-home-assistant-url/api")
    HA_TOKEN = os.getenv("HA_TOKEN", "your_static_token")

    # Signs the session cookie (issue #113). If unset, app.py generates a
    # random key at startup, which logs everyone out on every restart.
    SECRET_KEY = os.getenv("SECRET_KEY")
    # Set to False only for plain-HTTP development setups.
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "True").lower() in (
        "true",
        "1",
        "t",
    )
    SESSION_LIFETIME_HOURS = int(os.getenv("SESSION_LIFETIME_HOURS", "12"))

    # Number of reverse proxies in front of the backend whose X-Forwarded-*
    # headers are trusted (1 for the bundled nginx frontend proxy).
    TRUSTED_PROXY_HOPS = int(os.getenv("TRUSTED_PROXY_HOPS", "0"))
