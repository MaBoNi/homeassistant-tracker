"""
Defines all Flask routes for the Home Assistant Tracker API.
"""

from flask import request, jsonify
import requests
from sqlalchemy import text

from config.db import engine
from services.db_manager import get_gps_logs, get_unique_users
from . import api_bp
from .auth import token_required

import os

# Read environment variables
HA_TOKEN = os.getenv("HA_TOKEN")
HA_API_URL = os.getenv("HA_API_URL")


@api_bp.route('/gps-data', methods=['GET'])
@token_required
def get_gps_data():
    """
    Fetch GPS data based on user and time_range.
    """
    user = request.args.get('user')
    time_range = request.args.get('time_range', 'live')  # default to 'live'
    data = get_gps_logs(user, time_range)

    if not data:
        return jsonify({"message": "No data found!"}), 404

    return jsonify(data), 200


@api_bp.route('/users', methods=['GET'])
@token_required
def get_users():
    """
    Get a list of unique users with logged GPS data.
    """
    users = get_unique_users()

    if not users:
        return jsonify({"message": "No users found!"}), 404

    return jsonify(users), 200


@api_bp.route('/health', methods=['GET'])
def health_check():
    """
    Returns health status of Flask app, DB connection, and HA API.
    """
    health_status = {
        "flask_status": "OK",
        "db_status": "OK",
        "ha_status": "OK",
        "api_version": "0.9.0"
    }

    # Check database connection
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            if result.scalar() != 1:
                raise ValueError("Unexpected DB result")
    except Exception as db_error:  # Narrowed from `Exception`
        health_status["db_status"] = "ERROR"
        health_status["db_error"] = str(db_error)

    # Check Home Assistant API
    try:
        if not HA_TOKEN or not HA_API_URL:
            raise ValueError("Missing HA_TOKEN or HA_API_URL")

        headers = {
            'Authorization': f'Bearer {HA_TOKEN}',
            'Content-Type': 'application/json'
        }
        response = requests.get(f'{HA_API_URL}/states', headers=headers, timeout=5)
        if response.status_code != 200:
            raise ValueError(f'HA API returned {response.status_code}')
    except Exception as ha_error:
        health_status["ha_status"] = "ERROR"
        health_status["ha_error"] = str(ha_error)

    # Determine final HTTP status
    status_code = 200 if all(v == "OK" for v in health_status.values() if isinstance(v, str)) else 500
    return jsonify(health_status), status_code
