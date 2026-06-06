# backend/api/routes.py
"""
Defines all Flask routes for the Home Assistant Tracker API.
"""

import os
from datetime import datetime, time as dtime, timezone

from flask import request, jsonify
import requests
from sqlalchemy import text

from config.db import engine
from services.db_manager import (
    get_gps_logs,
    get_unique_users,
    get_devices_for_user,
    get_user_stats,
)
from . import api_bp
from .auth import token_required

# Read environment variables
HA_TOKEN = os.getenv("HA_TOKEN")
HA_API_URL = os.getenv("HA_API_URL")


def _parse_iso_date(value, end_of_day=False):
    """Parse an ISO date or datetime string. Returns datetime or None.

    Accepts ``YYYY-MM-DD`` (interpreted as midnight UTC, or 23:59:59.999999 UTC
    when ``end_of_day=True``) and full ISO-8601 timestamps (``end_of_day`` is
    ignored for those — the caller already specified the exact instant they
    want). Returns ``None`` if ``value`` is falsy. Raises ``ValueError`` on a
    malformed input so the caller can return HTTP 400.

    The ``end_of_day`` flag fixes the symmetric-single-day bug: a request like
    ``start_date=2026-06-01&end_date=2026-06-01`` would otherwise collapse to
    a single instant (midnight) and return no rows.
    """
    if not value:
        return None
    try:
        # date-only fast path
        if len(value) == 10 and value[4] == "-" and value[7] == "-":
            d = datetime.strptime(value, "%Y-%m-%d").date()
            t = dtime.max if end_of_day else dtime.min
            return datetime.combine(d, t, tzinfo=timezone.utc)
        # full ISO-8601; tolerate trailing 'Z'
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid ISO date: {value!r}") from exc


@api_bp.route("/gps-data", methods=["GET"])
@token_required
def get_gps_data():
    """
    Fetch GPS data based on user, optional time_range, and optional date range.

    Query parameters:
        user (str, required): The user whose logs to return.
        time_range (str): Relative time bucket (default ``live``). Ignored
            when ``start_date`` or ``end_date`` is supplied.
        start_date (str): ISO date/datetime, inclusive lower bound. Defaults
            to midnight UTC of the current day when neither bound is given
            and ``time_range`` is omitted.
        end_date (str): ISO date/datetime, inclusive upper bound.
    """
    user = request.args.get("user")
    time_range = request.args.get("time_range", "live")  # default to 'live'
    device = request.args.get("device") or None
    raw_start = request.args.get("start_date")
    raw_end = request.args.get("end_date")

    try:
        start_date = _parse_iso_date(raw_start)
        end_date = _parse_iso_date(raw_end, end_of_day=True)
    except ValueError:
        # Don't leak parser internals / user input back to the client.
        return jsonify({"error": "Invalid start_date or end_date (use YYYY-MM-DD)"}), 400

    # If the caller passed start_date but no end_date, treat end_date as the
    # end of that same day (so a single-day query is intuitive).
    if start_date and not end_date and raw_start and len(raw_start) == 10:
        end_date = start_date.replace(hour=23, minute=59, second=59, microsecond=999999)

    data = get_gps_logs(
        user,
        time_range,
        device=device,
        start_date=start_date,
        end_date=end_date,
    )

    # Always 200 — empty array is a valid result. Frontend renders the
    # "no logs in that range" message itself.
    return jsonify(data or []), 200


@api_bp.route("/users", methods=["GET"])
@token_required
def get_users():
    """
    Get a list of unique users with logged GPS data.
    """
    users = get_unique_users()

    if not users:
        return jsonify({"message": "No users found!"}), 404

    return jsonify(users), 200


@api_bp.route("/users/<username>/devices", methods=["GET"])
@token_required
def get_user_devices(username):
    """
    Get the distinct device identifiers ever seen for ``username``.

    Returns 200 with ``[]`` when the user has no devices (so the frontend can
    render a friendly empty-state rather than handling a 404).
    """
    devices = get_devices_for_user(username)
    return jsonify(devices or []), 200


@api_bp.route("/users/<username>/stats", methods=["GET"])
@token_required
def get_user_stats_route(username):
    """
    Per-user aggregate stats over an optional date window (issue #22).

    Query parameters:
        start_date, end_date — ISO date / datetime. Both optional.
    """
    raw_start = request.args.get("start_date")
    raw_end = request.args.get("end_date")
    try:
        start_date = _parse_iso_date(raw_start)
        end_date = _parse_iso_date(raw_end, end_of_day=True)
    except ValueError:
        # Don't leak parser internals / user input back to the client.
        return jsonify({"error": "Invalid start_date or end_date (use YYYY-MM-DD)"}), 400

    if start_date and not end_date and raw_start and len(raw_start) == 10:
        end_date = start_date.replace(hour=23, minute=59, second=59, microsecond=999999)

    stats = get_user_stats(username, start_date=start_date, end_date=end_date)
    return jsonify(stats), 200


@api_bp.route("/healthz", methods=["GET"])
def healthz():
    """
    Simple healthcheck endpoint for Docker that just verifies Flask is running.
    """
    return jsonify({"status": "healthy"}), 200


@api_bp.route("/health", methods=["GET"])
def health_check():
    """
    Returns detailed health status of Flask app, DB connection, and HA API.
    """
    health_status = {
        "flask_status": "OK",
        "db_status": "OK",
        "ha_status": "OK",
        "api_version": "0.9.0",
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
            "Authorization": f"Bearer {HA_TOKEN}",
            "Content-Type": "application/json",
        }
        response = requests.get(f"{HA_API_URL}/states", headers=headers, timeout=5)
        if response.status_code != 200:
            raise ValueError(f"HA API returned {response.status_code}")
    except Exception as ha_error:
        health_status["ha_status"] = "ERROR"
        health_status["ha_error"] = str(ha_error)

    # Determine final HTTP status
    status_code = (
        200
        if all(v == "OK" for v in health_status.values() if isinstance(v, str))
        else 500
    )
    return jsonify(health_status), status_code
