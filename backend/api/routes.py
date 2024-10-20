# backend/api/routes.py
from flask import request, jsonify
from . import api_bp
from .auth import token_required
from config.db import engine
import requests
from services.db_manager import get_gps_logs, get_unique_users

@api_bp.route('/gps-data', methods=['GET'])
@token_required
def get_gps_data():
    user = request.args.get('user')
    time_range = request.args.get('time_range', 'live')  # default to 'live'
    
    data = get_gps_logs(user, time_range)
    
    if not data:
        return jsonify({"message": "No data found!"}), 404

    return jsonify(data), 200

@api_bp.route('/users', methods=['GET'])
@token_required
def get_users():
    users = get_unique_users()

    if not users:
        return jsonify({"message": "No users found!"}), 404

    return jsonify(users), 200

@api_bp.route('/health', methods=['GET'])
def health_check():
    health_status = {
        "flask_status": "OK",
        "db_status": "OK",
        "ha_status": "OK",
        "api_version": "0.9.0"
    }

    # Check Database connection
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            if result.scalar() != 1:
                raise Exception("DB connection failed")
    except Exception as e:
        health_status["db_status"] = "ERROR"
        health_status["db_error"] = str(e)

    # Check Home Assistant API connection
    try:
        headers = {
            'Authorization': f'Bearer {HA_TOKEN}',
            'Content-Type': 'application/json'
        }
        response = requests.get(f'{HA_API_URL}/states', headers=headers, timeout=5)
        if response.status_code != 200:
            raise Exception(f'HA API returned {response.status_code}')
    except Exception as e:
        health_status["ha_status"] = "ERROR"
        health_status["ha_error"] = str(e)

    # Return health status and HTTP status code
    status_code = 200 if all(v == "OK" for v in health_status.values() if isinstance(v, str)) else 500
    return jsonify(health_status), status_code