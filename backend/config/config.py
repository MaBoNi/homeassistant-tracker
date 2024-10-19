# backend/config/config.py
import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:your_password@gps_tracker_db:5432/gps_tracker')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    HA_API_URL = os.getenv('HA_API_URL', 'http://your-home-assistant-url/api')
    HA_TOKEN = os.getenv('HA_TOKEN', 'your_static_token')
