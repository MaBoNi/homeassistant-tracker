# backend/app.py
"""
Flask application for Home Assistant Tracker.
"""

import os
from flask import Flask
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
# Only allow requests from the frontend domain and localhost for development
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:5172",
            "http://127.0.0.1:5172",
            # Add your production frontend domain here when deployed
            # "https://yourdomain.com"
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Authorization", "Content-Type"],
        "expose_headers": ["Content-Type"],
        "supports_credentials": False,
        "max_age": 600
    }
})

app.register_blueprint(api_bp, url_prefix="/api")

# Configure rate limiting to prevent API abuse
# Default limits apply to all routes: 200 per day, 50 per hour
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",  # In-memory storage (use Redis for production)
    strategy="fixed-window"
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
