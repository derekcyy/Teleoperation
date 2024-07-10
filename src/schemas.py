from pydantic import BaseModel
from datetime import datetime

class TelemetryCreate(BaseModel):
    turtleBotId: int
    timestamp: datetime
    x: float
    y: float
    heading: float
