"""
API Blueprint Initialization for Home Assistant Tracker.
"""

from flask import Blueprint

api_bp = Blueprint('api', __name__)

# Import routes to register endpoints AFTER api_bp is defined.
# noqa tells linters it's intentional and should not be moved.
from . import routes  # noqa: C0413, F401
