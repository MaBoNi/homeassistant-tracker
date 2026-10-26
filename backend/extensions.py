# backend/extensions.py
"""
Flask extensions created without an app so blueprints can import them
(e.g. ``@limiter.limit``) before ``app.py`` calls ``init_app``.
"""

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Default limits apply to all routes: 200 per day, 50 per hour
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",  # In-memory storage (use Redis for production)
    strategy="fixed-window",
)
