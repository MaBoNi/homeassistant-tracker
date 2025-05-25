# backend/services/ha_fetcher.py

"""
Service to fetch GPS data from Home Assistant API and store it in the database.
"""

import os
import logging
from datetime import datetime

import requests

from .db_manager import save_gps_log

# Load Home Assistant API credentials from environment
HA_API_URL = os.getenv('HA_API_URL', 'http://your-home-assistant-url/api')
HA_TOKEN = os.getenv('HA_TOKEN', 'your_static_token')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def fetch_and_save_location(user_entity):
    """
    Fetch location data for a Home Assistant user and save it using save_gps_log.

    Args:
        user_entity (str): Home Assistant entity ID for a person (e.g. 'person.martin')
    """
    url = f"{HA_API_URL}/states/{user_entity}"
    headers = {"Authorization": f"Bearer {HA_TOKEN}"}

    logger.info("Fetching location for %s from Home Assistant API: %s", user_entity, url)

    try:
        response = requests.get(url, headers=headers)
        logger.info("Response Status Code for %s: %s", user_entity, response.status_code)

        if response.status_code == 200:
            data = response.json()
            attributes = data.get('attributes', {})
            device_trackers = attributes.get('device_trackers', [])

            for device_tracker in device_trackers:
                logger.info("Found device_tracker for %s: %s", user_entity, device_tracker)

                device_tracker_url = f"{HA_API_URL}/states/{device_tracker}"
                device_response = requests.get(device_tracker_url, headers=headers)
                logger.info("Response Status Code for %s: %s", device_tracker, device_response.status_code)

                if device_response.status_code == 200:
                    device_data = device_response.json()
                    device_attributes = device_data.get('attributes', {})

                    latitude = device_attributes.get('latitude')
                    longitude = device_attributes.get('longitude')
                    accuracy = device_attributes.get('gps_accuracy')
                    timestamp = datetime.utcnow()

                    if latitude and longitude:
                        logger.info(
                            "Received location data for %s: Latitude %s, Longitude %s",
                            device_tracker, latitude, longitude
                        )

                        user_without_prefix = user_entity.replace('person.', '')

                        save_gps_log(
                            user_without_prefix,
                            device_tracker,
                            latitude,
                            longitude,
                            accuracy,
                            timestamp
                        )
                    else:
                        logger.warning("No location data available for %s", device_tracker)
                else:
                    logger.error(
                        "Failed to fetch data for %s. Status Code: %s",device_tracker, device_response.status_code
                    )
                    logger.error(
                        "Device tracker URL: %s", device_tracker_url
                    )
                    logger.error(
                        "Headers: %s", headers
                    )
        else:
            logger.error(
                "Failed to fetch data for %s. Status Code: %s", user_entity, response.status_code
            )
            logger.error(
                "Request URL: %s", url
            )
            logger.error(
                "Headers: %s", headers
            )

    except Exception as e:
        logger.error(
            "Error occurred while fetching data for %s: %s", user_entity, str(e)
        )
        logger.error(
            "Request URL: %s", url
        )
        logger.error(
            "Headers: %s", headers
        )
