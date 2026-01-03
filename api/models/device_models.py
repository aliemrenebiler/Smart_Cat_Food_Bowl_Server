from pydantic import BaseModel


class CreateDeviceRequest(BaseModel):
    name: str
    model: str = "food_bowl"


class GetDeviceResponse(BaseModel):
    id: str
    name: str
    model: str
    info_topic: str
    control_topic: str
