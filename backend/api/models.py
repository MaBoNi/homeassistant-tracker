# backend/api/models.py
"""
Database models for Home Assistant Tracker.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime
from config.db import Base

class GPSLog(Base):
    """
    Represents a GPS log entry stored in the database.
    Tracks user movement with timestamps and accuracy details.
    """

    __tablename__ = "gps_logs"

    id = Column(Integer, primary_key=True)
    user = Column(String, nullable=False)
    device = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    accuracy = Column(Float, nullable=True)

    def to_dict(self) -> dict:
        """
        Convert the GPS log entry to a dictionary format.

        Returns:
            dict: A dictionary representation of the GPS log entry.
        """
        return {
            "user": self.user,
            "device": self.device,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "timestamp": self.timestamp.isoformat(),
            "accuracy": self.accuracy,
        }

    def __repr__(self) -> str:
        """
        String representation of the GPSLog object.

        Returns:
            str: Readable representation of the GPS log entry.
        """
        return f"<GPSLog user={self.user} device={self.device} timestamp={self.timestamp}>"
