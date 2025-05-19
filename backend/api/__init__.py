# backend/api/__init__.py
"""
API Blueprint Initialization for Home Assistant Tracker.
"""

from flask import Blueprint
from . import routes

api_bp = Blueprint('api', __name__)
