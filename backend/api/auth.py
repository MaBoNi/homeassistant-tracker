# backend/api/auth.py
"""
Authentication utilities for protecting Flask routes using a bearer token.
"""

import os
from functools import wraps
from flask import request, jsonify

# Fetch the TRACKER_APP_TOKEN from the environment
BEARER_TOKEN = os.getenv('TRACKER_APP_TOKEN')

def token_required(f):
    """
    Decorator to enforce bearer token authentication for protected routes.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or token != f"Bearer {BEARER_TOKEN}":
            return jsonify({"message": "Authentication is required!"}), 401
        return f(*args, **kwargs)
    return decorated_function
