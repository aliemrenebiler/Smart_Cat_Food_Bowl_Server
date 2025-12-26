from datetime import datetime
import uuid

from sqlalchemy import Column, Integer, String, DateTime

from db.database import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    @property
    def info_topic(self):
        return f"devices/{self.id}/info"

    @property
    def control_topic(self):
        return f"devices/{self.id}/control/#"


class DeviceData(Base):
    __tablename__ = "device_data"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String, index=True)
    topic = Column(String)
    payload = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
