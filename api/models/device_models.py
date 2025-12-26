from pydantic import BaseModel


class CreateDeviceRequest(BaseModel):
    name: str


class GetDeviceResponse(BaseModel):
    id: str
    name: str
    info_topic: str
    control_topic: str
