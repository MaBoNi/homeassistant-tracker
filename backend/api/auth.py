# backend/api/auth.py
from flask import request, jsonify
from functools import wraps

BEARER_TOKEN = "your_static_token"  # Change this to your actual static token

def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token or token != f"Bearer {BEARER_TOKEN}":
            return jsonify({"message": "Authentication is required!"}), 401
        return f(*args, **kwargs)
    return decorated_function
