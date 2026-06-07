# backend/app.py
"""
Flask application for Home Assistant Tracker.
"""

import os
from flask import Flask, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from apscheduler.schedulers.background import BackgroundScheduler

from api import api_bp
from config.db import init_db
from services.ha_fetcher import fetch_and_save_location

# Initialize the database (option to drop the database on start)
drop_db_on_start = os.getenv("DROP_DB_ON_START", "False").lower() in ("true", "1", "t")
init_db(drop_and_recreate=drop_db_on_start)

app = Flask(__name__)

# Configure CORS with restricted origins for security
# Read allowed origins from environment variable (comma-separated)
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5172,http://127.0.0.1:5172")
allowed_origins = [origin.strip() for origin in cors_origins.split(",")]

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": allowed_origins,
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Authorization", "Content-Type"],
            "expose_headers": ["Content-Type", "Sunset", "Deprecation", "Link"],
            "supports_credentials": False,
            "max_age": 600,
        }
    },
)

# Register the API blueprint under the versioned prefix (canonical) and the
# legacy bare /api prefix (deprecated alias kept for one release cycle, see
# docs/api/versioning.md).
app.register_blueprint(api_bp, url_prefix="/api/v1")
app.register_blueprint(api_bp, name="api_legacy", url_prefix="/api")


# Sunset / Deprecation date for the legacy /api/* alias. ~12 months from the
# introduction of /api/v1 (issue #78).
LEGACY_API_SUNSET = "Sun, 06 Jun 2027 00:00:00 GMT"


@app.after_request
def _tag_legacy_api(response):
    """
    Add Sunset / Deprecation / Link headers on responses served from the
    legacy /api/* prefix so clients can detect the deprecation in CI / logs
    and migrate to /api/v1/*. The versioned prefix is left untouched.
    """
    path = request.path or ""
    if path.startswith("/api/") and not path.startswith("/api/v1/"):
        response.headers["Deprecation"] = "true"
        response.headers["Sunset"] = LEGACY_API_SUNSET
        # RFC 8288 Link header pointing to the successor resource.
        successor = path.replace("/api/", "/api/v1/", 1)
        response.headers["Link"] = f'<{successor}>; rel="successor-version"'
    return response


# Configure rate limiting to prevent API abuse
# Default limits apply to all routes: 200 per day, 50 per hour
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",  # In-memory storage (use Redis for production)
    strategy="fixed-window",
)

scheduler = BackgroundScheduler()


def get_users_to_track():
    """
    Read HA_USERS from environment variables and append 'person.' prefix.

    Returns:
        list: A list of formatted Home Assistant user IDs.
    """
    users = os.getenv("HA_USERS", "")
    return [f"person.{user.strip()}" for user in users.split(",") if user]


users_to_track = get_users_to_track()


def fetch_gps_data():
    """
    Fetch GPS data for each user listed in HA_USERS.
    """
    for user in users_to_track:
        fetch_and_save_location(user)


# Schedule periodic GPS data fetching
scheduler.add_job(func=fetch_gps_data, trigger="interval", seconds=30)
scheduler.start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
