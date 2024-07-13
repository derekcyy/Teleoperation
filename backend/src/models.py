from pydantic import BaseModel
from typing import List

class TelemetryCreate(BaseModel):
    turtleBotId: int
    timestamp: str
    x: float
    y: float
    heading: float

class BatteryCreate(BaseModel):
    turtleBotId: int
    timestamp: str
    voltage: float
    current: float
    percentage: float

class CameraCreate(BaseModel):
    turtleBotId: int
    timestamp: str
    image: bytes

class LidarCreate(BaseModel):
    turtleBotId: int
    timestamp: str
    ranges: List[float]
