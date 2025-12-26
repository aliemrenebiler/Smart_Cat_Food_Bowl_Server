from sqlalchemy.orm import Session

from db.models.device_models import Device, DeviceData


class DeviceService:
    def __init__(self, db: Session):
        self.db = db

    def create_device(self, name: str) -> Device:
        new_device = Device(name=name)
        self.db.add(new_device)
        self.db.commit()
        self.db.refresh(new_device)
        return new_device

    def get_all_devices(self) -> list[Device]:
        return self.db.query(Device).all()

    def delete_device(self, device_id: str):
        db_device = self.db.query(Device).filter(Device.id == device_id).first()
        if not db_device:
            raise ValueError("Device not found")
        self.db.delete(db_device)
        self.db.commit()

    def create_device_data(self, device_id: str, topic: str, payload: str):
        new_data = DeviceData(device_id=device_id, topic=topic, payload=payload)
        self.db.add(new_data)
        self.db.commit()

    def get_device_data(self, device_id: str) -> list[DeviceData]:
        return self.db.query(DeviceData).filter(DeviceData.device_id == device_id).all()
