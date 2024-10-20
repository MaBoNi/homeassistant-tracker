# backend/api/auth.py
import os
from flask import request, jsonify
from functools import wraps

# Fetch the TRACKER_APP_TOKEN from the environment
BEARER_TOKEN = os.getenv('TRACKER_APP_TOKEN')

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or token != f"Bearer {BEARER_TOKEN}":
            return jsonify({"message": "Authentication is required!"}), 401
        return f(*args, **kwargs)
    return decorated_function
