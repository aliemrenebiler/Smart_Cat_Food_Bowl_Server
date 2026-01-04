from datetime import datetime, timezone
import uuid

from sqlalchemy import Column, String, DateTime, ForeignKey

from db.database import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String)
    model = Column(String, default="food_bowl")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    @property
    def info_topic(self):
        return "devices/bowl/info"
        # return f"devices/{self.id}/info"

    @property
    def control_topic(self):
        return "devices/bowl/control"
        # return f"devices/{self.id}/control"


class DeviceData(Base):
    __tablename__ = "device_data"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    device_id = Column(String, ForeignKey("devices.id"), index=True)
    topic = Column(String)
    payload = Column(String)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
