# backend/services/ha_fetcher.py
import requests
import logging
from datetime import datetime
from .db_manager import save_gps_log
import os


HA_API_URL=os.getenv('HA_API_URL', 'http://your-home-assistant-url/api')
HA_TOKEN=os.getenv('HA_TOKEN',  'your_static_token')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_and_save_location(user_entity):
    # Append /states/ to the HA_API_URL to construct the full URL for fetching entity states
    url = f"{HA_API_URL}/states/{user_entity}"
    headers = {"Authorization": f"Bearer {HA_TOKEN}"}
    
    logger.info(f"Fetching location for {user_entity} from Home Assistant API: {url}")

    try:
        # Step 1: Fetch the person entity data
        response = requests.get(url, headers=headers)
        logger.info(f"Response Status Code for {user_entity}: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            attributes = data.get('attributes', {})
            device_trackers = attributes.get('device_trackers', [])

            if device_trackers:
                device_tracker = device_trackers[0]  # Use the first device_tracker available
                logger.info(f"Found device_tracker for {user_entity}: {device_tracker}")

                # Step 2: Fetch the actual location data from the device_tracker
                device_tracker_url = f"{HA_API_URL}/states/{device_tracker}"
                device_response = requests.get(device_tracker_url, headers=headers)
                logger.info(f"Response Status Code for {device_tracker}: {device_response.status_code}")

                if device_response.status_code == 200:
                    device_data = device_response.json()
                    device_attributes = device_data.get('attributes', {})
                    
                    latitude = device_attributes.get('latitude')
                    longitude = device_attributes.get('longitude')
                    accuracy = device_attributes.get('gps_accuracy')
                    timestamp = datetime.utcnow()  # Use current time as timestamp

                    if latitude and longitude:
                        logger.info(f"Received location data for {device_tracker}: Latitude {latitude}, Longitude {longitude}")

                        # Strip 'person.' from user_entity before saving
                        user_without_prefix = user_entity.replace('person.', '')

                        # Save the GPS log, including the device tracker
                        save_gps_log(user_without_prefix, device_tracker, latitude, longitude, accuracy, timestamp)
                    else:
                        logger.warning(f"No location data available for {device_tracker}")
                else:
                    # Log detailed error information when fetching device_tracker fails
                    logger.error(f"Failed to fetch data for {device_tracker}. Status Code: {device_response.status_code}")
                    logger.error(f"Device tracker URL: {device_tracker_url}")
                    logger.error(f"Headers: {headers}")
            else:
                logger.warning(f"No device_tracker found for {user_entity}")
        else:
            # Log detailed error information when fetching user entity fails
            logger.error(f"Failed to fetch data for {user_entity}. Status Code: {response.status_code}")
            logger.error(f"Request URL: {url}")
            logger.error(f"Headers: {headers}")
    except Exception as e:
        # Log any exceptions that occur during the API request
        logger.error(f"Error occurred while fetching data for {user_entity}: {str(e)}")
        logger.error(f"Request URL: {url}")
        logger.error(f"Headers: {headers}")
