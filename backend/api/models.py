# backend/api/models.py
from sqlalchemy import Column, Integer, String, Float, DateTime
from config.db import Base

class GPSLog(Base):
    __tablename__ = 'gps_logs'
    
    id = Column(Integer, primary_key=True)
    user = Column(String, nullable=False)
    device = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    accuracy = Column(Float, nullable=True)

    def to_dict(self):
        return {
            'user': self.user,
            'device': self.device,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'timestamp': self.timestamp.isoformat(),
            'accuracy': self.accuracy
        }
