# backend/services/db_manager.py
import logging
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, desc
from datetime import datetime, timedelta
from api.models import GPSLog
from config.db import Base, engine
from config.config import Config
from datetime import timezone

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Session = sessionmaker(bind=engine)
session = Session()

def save_gps_log(user, device, latitude, longitude, accuracy, timestamp):
    # Strip 'person.' prefix from the user if present
    if user.startswith('person.'):
        user = user.replace('person.', '')

    # Strip 'device_tracker.' prefix from the device if present
    if device.startswith('device_tracker.'):
        device = device.replace('device_tracker.', '')

    logger.info(f"Attempting to save GPS log for user: {user} and device: {device} with coordinates ({latitude}, {longitude})")

    try:
        # Check if the new data is different from the last saved data
        last_log = session.query(GPSLog).filter_by(user=user, device=device).order_by(desc(GPSLog.timestamp)).first()

        if last_log:
            logger.info(f"Last saved location for {user} on device {device}: Latitude {last_log.latitude}, Longitude {last_log.longitude}, Timestamp: {last_log.timestamp}")

        if last_log and (last_log.latitude == latitude and last_log.longitude == longitude):
            logger.info(f"No change in location for {user} on device {device}, skipping save.")
            return  # No change, skip saving

        new_log = GPSLog(
            user=user,
            device = device.replace('device_tracker.', '').lower(),
            latitude=latitude,
            longitude=longitude,
            accuracy=accuracy,
            timestamp=timestamp
        )
        session.add(new_log)
        session.commit()
        logger.info(f"Saved GPS log for user: {user} and device: {device} at {timestamp}")

    except Exception as e:
        # Roll back the session on error
        session.rollback()
        logger.error(f"Error saving GPS log for user: {user} on device: {device}: {str(e)}")

def get_gps_logs(user, time_range, device=None):
    try:
        # Strip 'person.' from the user if present
        if user.startswith('person.'):
            user = user.replace('person.', '')

        logger.info(f"Retrieving GPS logs for user: {user} with time range: {time_range}")

        query = session.query(GPSLog).filter_by(user=user)
        
        # Apply time filters
        if time_range == 'last_hour':
            time_limit = datetime.now(timezone.utc) - timedelta(hours=1)
        elif time_range == 'last_2_hours':
            time_limit = datetime.now(timezone.utc) - timedelta(hours=2)
        elif time_range == 'last_3_hours':
            time_limit = datetime.now(timezone.utc) - timedelta(hours=3)
        elif time_range == 'last_6_hours':
            time_limit = datetime.now(timezone.utc) - timedelta(hours=6)
        elif time_range == 'last_day':
            time_limit = datetime.now(timezone.utc) - timedelta(days=1)
        elif time_range == 'last_7_days':
            time_limit = datetime.now(timezone.utc) - timedelta(days=7)
        elif time_range == 'last_30_days':
            time_limit = datetime.now(timezone.utc) - timedelta(days=30)
        else:
            time_limit = None  # live (get the most recent entry)

        if device:
            logger.info(f"Applying device filter: {device.lower()}")
            query = query.filter_by(device=device.lower())

        if device:
            logger.info(f"Applying device filter: {device.lower()}")
            query = query.filter_by(device=device.lower())

        if time_limit:
            logger.info(f"Applying time filter: {time_limit}")
            query = query.filter(GPSLog.timestamp > time_limit)
        
        # Log the SQL query being executed
        logger.info(f"Executing query: {str(query)}")

        logs = query.order_by(GPSLog.timestamp).all()
        
        if not logs:
            logger.info(f"No GPS logs found for user: {user}")
        else:
            logger.info(f"Found {len(logs)} logs for user: {user}")

        return [log.to_dict() for log in logs]

    except Exception as e:
        session.rollback()
        logger.error(f"Error retrieving GPS logs for user: {user}: {str(e)}")

def get_unique_users():
    try:
        users = session.query(GPSLog.user).distinct().all()
        user_list = [user[0] for user in users]  # Extract user names from query results

        if not user_list:
            logger.info("No users found in GPS logs.")
        else:
            logger.info(f"Found {len(user_list)} unique users.")

        return user_list

    except Exception as e:
        session.rollback()
        logger.error(f"Error retrieving unique users: {str(e)}")
        return []
