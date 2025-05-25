"""
API Blueprint Initialization for Home Assistant Tracker.
"""

from flask import Blueprint

api_bp = Blueprint('api', __name__)

from . import routes
