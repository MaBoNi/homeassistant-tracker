# backend/services/db_manager.py
"""
Handles database interactions for GPS log storage and retrieval.
"""

import logging
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc, text

from api.models import GPSLog
from config.db import engine

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Session = sessionmaker(bind=engine)
session = Session()


def save_gps_log(user, device, latitude, longitude, accuracy, timestamp):
    """
    Save a new GPS log entry if the location has changed.

    Args:
        user (str): Username (stripped of 'person.')
        device (str): Device name (stripped of 'device_tracker.')
        latitude (float): Latitude
        longitude (float): Longitude
        accuracy (float): Accuracy of the GPS reading
        timestamp (datetime): Time of the reading
    """
    if user.startswith('person.'):
        user = user.replace('person.', '')

    if device.startswith('device_tracker.'):
        device = device.replace('device_tracker.', '')

    logger.info(
        "Attempting to save GPS log for user: %s and device: %s with coordinates (%s, %s)",
        user, device, latitude, longitude
    )

    try:
        last_log = (
            session.query(GPSLog)
            .filter_by(user=user, device=device)
            .order_by(desc(GPSLog.timestamp))
            .first()
        )

        if last_log:
            logger.info(
                "Last saved location for %s on device %s: Latitude %s, Longitude %s, Timestamp: %s",
                user, device, last_log.latitude, last_log.longitude, last_log.timestamp
            )

        if last_log and last_log.latitude == latitude and last_log.longitude == longitude:
            logger.info(
                "No change in location for %s on device %s, skipping save.",
                user, device
            )
            return

        new_log = GPSLog(
            user=user,
            device=device.lower(),
            latitude=latitude,
            longitude=longitude,
            accuracy=accuracy,
            timestamp=timestamp
        )
        session.add(new_log)
        session.commit()
        logger.info(
            "Saved GPS log for user: %s and device: %s at %s",
            user, device, timestamp
        )

    except Exception as e:
        session.rollback()
        logger.error(
            "Error saving GPS log for user: %s on device: %s: %s",
            user, device, str(e)
        )


def get_gps_logs(user, time_range, device=None):
    """
    Retrieve GPS logs for a given user and optional device/time range.

    Args:
        user (str): Username (stripped of 'person.')
        time_range (str): A time window like 'last_hour', 'last_day', etc.
        device (str, optional): Specific device to filter by.

    Returns:
        list: List of GPS logs as dictionaries.
    """
    try:
        if user.startswith('person.'):
            user = user.replace('person.', '')

        logger.info("Retrieving GPS logs for user: %s with time range: %s", user, time_range)

        query = session.query(GPSLog).filter_by(user=user)

        # Time filter
        time_map = {
            'last_hour': timedelta(hours=1),
            'last_2_hours': timedelta(hours=2),
            'last_3_hours': timedelta(hours=3),
            'last_6_hours': timedelta(hours=6),
            'last_day': timedelta(days=1),
            'last_7_days': timedelta(days=7),
            'last_30_days': timedelta(days=30),
        }

        time_limit = datetime.now(timezone.utc) - time_map.get(time_range, timedelta(0))
        if time_range != 'live':
            logger.info("Applying time filter: %s", time_limit)
            query = query.filter(GPSLog.timestamp > time_limit)

        if device:
            logger.info("Applying device filter: %s", device.lower())
            query = query.filter_by(device=device.lower())

        logger.info("Executing query")
        logs = query.order_by(GPSLog.timestamp).all()

        if not logs:
            logger.info("No GPS logs found for user: %s", user)
        else:
            logger.info("Found %d logs for user: %s", len(logs), user)

        return [log.to_dict() for log in logs]

    except Exception as e:
        session.rollback()
        logger.error("Error retrieving GPS logs for user: %s: %s", user, str(e))


def get_unique_users():
    """
    Get list of unique users from the GPS logs.

    Returns:
        list: List of user strings.
    """
    try:
        users = session.query(GPSLog.user).distinct().all()
        user_list = [user[0] for user in users]

        if not user_list:
            logger.info("No users found in GPS logs.")
        else:
            logger.info("Found %d unique users.", len(user_list))

        return user_list

    except Exception as e:
        session.rollback()
        logger.error("Error retrieving unique users: %s", str(e))
        return []
