# backend/api/auth.py
"""
Authentication utilities for protecting Flask routes using a bearer token.
"""

import os
import secrets
import logging
from functools import wraps
from flask import request, jsonify

# Set up logging
logger = logging.getLogger(__name__)

# Fetch the TRACKER_APP_TOKEN from the environment
BEARER_TOKEN = os.getenv('TRACKER_APP_TOKEN')

def token_required(f):
    """
    Decorator to enforce bearer token authentication for protected routes.
    Uses constant-time comparison to prevent timing attacks.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')

        # Log failed attempts (without token details)
        if not token:
            logger.warning(f"Authentication attempt without token from {request.remote_addr}")
            return jsonify({"message": "Authentication is required"}), 401

        # Extract Bearer token
        if not token.startswith("Bearer "):
            logger.warning(f"Invalid auth header format from {request.remote_addr}")
            return jsonify({"message": "Invalid authentication format"}), 401

        provided_token = token[7:]  # Remove "Bearer " prefix

        # Use constant-time comparison to prevent timing attacks
        if not secrets.compare_digest(provided_token, BEARER_TOKEN):
            logger.warning(f"Failed authentication attempt from {request.remote_addr}")
            return jsonify({"message": "Invalid authentication credentials"}), 401

        return f(*args, **kwargs)
    return decorated_function
