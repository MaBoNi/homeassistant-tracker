# backend/api/gdpr.py
"""
GDPR compliance endpoints (issue #75).

Provides per-user data export, deletion ("right to be forgotten"), and
consent read/write under the canonical ``/api/v1/users/<username>/...``
prefix. All endpoints require the existing bearer-token auth.
"""

import csv
import io
import logging
from datetime import datetime, timezone

from flask import jsonify, request, Response, stream_with_context
from sqlalchemy.orm import sessionmaker

from api.models import GPSLog, UserConsent
from config.db import engine
from . import api_bp
from .auth import token_required

logger = logging.getLogger(__name__)

Session = sessionmaker(bind=engine)


@api_bp.route("/users/<username>/data", methods=["DELETE"])
@token_required
def delete_user_data(username):
    """
    Delete all GPSLog rows for ``username`` (GDPR Art. 17, right to erasure).

    Returns the number of rows removed. Consent rows are kept so the user's
    withdrawal-of-consent record survives erasure of location history.
    """
    s = Session()
    try:
        deleted = s.query(GPSLog).filter(GPSLog.user == username).delete(
            synchronize_session=False
        )
        s.commit()
        logger.info("GDPR: erased %d GPS rows for user=%s", deleted, username)
        return jsonify({"username": username, "deleted_rows": deleted}), 200
    except Exception as exc:  # pragma: no cover - defensive
        s.rollback()
        logger.exception("GDPR erase failed for %s", username)
        return jsonify({"error": "internal_error"}), 500
    finally:
        s.close()


def _rows_for_user(username):
    s = Session()
    try:
        rows = (
            s.query(GPSLog)
            .filter(GPSLog.user == username)
            .order_by(GPSLog.timestamp.asc())
            .all()
        )
        return [r.to_dict() for r in rows]
    finally:
        s.close()


@api_bp.route("/users/<username>/export", methods=["GET"])
@token_required
def export_user_data(username):
    """
    Export all GPSLog rows for ``username`` (GDPR Art. 20, data portability).

    Query parameters:
        format: ``json`` (default) or ``csv``.
    """
    fmt = (request.args.get("format") or "json").lower()
    rows = _rows_for_user(username)

    if fmt == "csv":
        def generate():
            buf = io.StringIO()
            writer = csv.writer(buf)
            writer.writerow(
                ["user", "device", "latitude", "longitude", "timestamp", "accuracy"]
            )
            yield buf.getvalue()
            buf.seek(0)
            buf.truncate(0)
            for r in rows:
                writer.writerow(
                    [
                        r["user"],
                        r["device"],
                        r["latitude"],
                        r["longitude"],
                        r["timestamp"],
                        r["accuracy"],
                    ]
                )
                yield buf.getvalue()
                buf.seek(0)
                buf.truncate(0)

        filename = f"{username}-gps-export.csv"
        return Response(
            stream_with_context(generate()),
            mimetype="text/csv",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )

    if fmt != "json":
        return jsonify({"error": "format must be json or csv"}), 400

    return jsonify({"username": username, "count": len(rows), "rows": rows}), 200


@api_bp.route("/users/<username>/consent", methods=["GET"])
@token_required
def get_user_consent(username):
    """
    Read the consent record for ``username``. Returns a default
    no-consent record if none has ever been stored.
    """
    s = Session()
    try:
        row = s.get(UserConsent, username)
        if row is None:
            return (
                jsonify(
                    {
                        "username": username,
                        "has_consent": False,
                        "consent_given_at": None,
                        "consent_withdrawn_at": None,
                        "policy_version": None,
                    }
                ),
                200,
            )
        return jsonify(row.to_dict()), 200
    finally:
        s.close()


@api_bp.route("/users/<username>/consent", methods=["POST"])
@token_required
def set_user_consent(username):
    """
    Record or withdraw consent for ``username``.

    Body: ``{ "consent": true|false, "policy_version": "1.0" }``.
    """
    data = request.get_json(silent=True) or {}
    consent = bool(data.get("consent"))
    policy_version = data.get("policy_version")
    now = datetime.now(timezone.utc).replace(tzinfo=None)

    s = Session()
    try:
        row = s.get(UserConsent, username)
        if row is None:
            row = UserConsent(username=username)
            s.add(row)
        row.has_consent = consent
        if consent:
            row.consent_given_at = now
            row.consent_withdrawn_at = None
        else:
            row.consent_withdrawn_at = now
        if policy_version:
            row.policy_version = str(policy_version)
        s.commit()
        s.refresh(row)
        return jsonify(row.to_dict()), 200
    except Exception as exc:  # pragma: no cover - defensive
        s.rollback()
        logger.exception("GDPR consent write failed for %s", username)
        return jsonify({"error": "internal_error"}), 500
    finally:
        s.close()
