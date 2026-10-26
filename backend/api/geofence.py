# backend/api/geofence.py
"""
Geofence zone CRUD (issue #116) under ``/api/v1/users/<username>/zones``.

``<username>`` is the tracked Home Assistant person. Everyone may read their
own zones; ``user`` accounts may also create, rename, toggle and delete them;
admins and the legacy bearer token may act on anyone (``@require_role``).
Point-in-zone evaluation is #117.
"""

import logging

from flask import jsonify, request
from sqlalchemy.orm import sessionmaker

from api.models import GeofenceZone
from config.db import engine
from . import api_bp
from .auth import require_role

logger = logging.getLogger(__name__)

Session = sessionmaker(bind=engine)

RADIUS_MIN_M = 10
RADIUS_MAX_M = 50000
MAX_ZONES_PER_USER = 50
NAME_MAX_LEN = 100


def _number(value):
    """Accept ints and floats but not bools (``True`` is an int in Python)."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _validate_name(name):
    if not isinstance(name, str) or not name.strip() or len(name.strip()) > NAME_MAX_LEN:
        return f"name must be 1-{NAME_MAX_LEN} characters"
    return None


def _validate_new_zone(data):
    """Return an error message for a POST body, or None if valid."""
    error = _validate_name(data.get("name"))
    if error:
        return error
    lat, lon, radius = data.get("center_lat"), data.get("center_lon"), data.get("radius_m")
    if not _number(lat) or not -90 <= lat <= 90:
        return "center_lat must be a number between -90 and 90"
    if not _number(lon) or not -180 <= lon <= 180:
        return "center_lon must be a number between -180 and 180"
    if not _number(radius) or not RADIUS_MIN_M <= radius <= RADIUS_MAX_M:
        return f"radius_m must be a number between {RADIUS_MIN_M} and {RADIUS_MAX_M}"
    if "active" in data and not isinstance(data["active"], bool):
        return "active must be true or false"
    return None


def _json_body():
    data = request.get_json(silent=True)
    return data if isinstance(data, dict) else {}


@api_bp.route("/users/<username>/zones", methods=["GET"])
@require_role("user", "readonly", own_kwarg="username")
def list_zones(username):
    """List all zones (active and inactive) for ``username``, oldest first."""
    s = Session()
    try:
        zones = (
            s.query(GeofenceZone)
            .filter(GeofenceZone.owner_user == username)
            .order_by(GeofenceZone.id)
            .all()
        )
        return jsonify([z.to_dict() for z in zones]), 200
    finally:
        s.close()


@api_bp.route("/users/<username>/zones", methods=["POST"])
@require_role("user", own_kwarg="username")
def create_zone(username):
    """
    Body: ``{ name, center_lat, center_lon, radius_m, active? }``.
    Returns 201 with the zone, 400 on invalid input, 409 at the per-user limit.
    """
    data = _json_body()
    error = _validate_new_zone(data)
    if error:
        return jsonify({"message": error}), 400

    s = Session()
    try:
        count = s.query(GeofenceZone).filter(GeofenceZone.owner_user == username).count()
        if count >= MAX_ZONES_PER_USER:
            return (
                jsonify({"message": f"A user can have at most {MAX_ZONES_PER_USER} zones"}),
                409,
            )
        zone = GeofenceZone(
            owner_user=username,
            name=data["name"].strip(),
            geometry_type="circle",
            center_lat=float(data["center_lat"]),
            center_lon=float(data["center_lon"]),
            radius_m=float(data["radius_m"]),
            active=data.get("active", True),
        )
        s.add(zone)
        s.commit()
        logger.info(f"Created geofence zone {zone.id} '{zone.name}' for {username}")
        return jsonify(zone.to_dict()), 201
    finally:
        s.close()


@api_bp.route("/users/<username>/zones/<int:zone_id>", methods=["PATCH"])
@require_role("user", own_kwarg="username")
def update_zone(username, zone_id):
    """Rename and/or toggle a zone. Body: ``{ name?, active? }``."""
    data = _json_body()
    changes = {}
    if "name" in data:
        error = _validate_name(data["name"])
        if error:
            return jsonify({"message": error}), 400
        changes["name"] = data["name"].strip()
    if "active" in data:
        if not isinstance(data["active"], bool):
            return jsonify({"message": "active must be true or false"}), 400
        changes["active"] = data["active"]
    if not changes:
        return jsonify({"message": "Nothing to update (name, active)"}), 400

    s = Session()
    try:
        zone = s.get(GeofenceZone, zone_id)
        # 404 for another person's zone too, so ids don't leak across users.
        if zone is None or zone.owner_user != username:
            return jsonify({"message": "Zone not found"}), 404
        for field, value in changes.items():
            setattr(zone, field, value)
        s.commit()
        return jsonify(zone.to_dict()), 200
    finally:
        s.close()


@api_bp.route("/users/<username>/zones/<int:zone_id>", methods=["DELETE"])
@require_role("user", own_kwarg="username")
def delete_zone(username, zone_id):
    """Delete a zone. Returns 200 with the deleted id, or 404."""
    s = Session()
    try:
        zone = s.get(GeofenceZone, zone_id)
        if zone is None or zone.owner_user != username:
            return jsonify({"message": "Zone not found"}), 404
        s.delete(zone)
        s.commit()
        logger.info(f"Deleted geofence zone {zone_id} for {username}")
        return jsonify({"deleted": zone_id}), 200
    finally:
        s.close()
