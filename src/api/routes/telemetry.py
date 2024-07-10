from fastapi import APIRouter
from pydantic import BaseModel
from src.database import db

router = APIRouter()

class TelemetryData(BaseModel):
    turtleBotId: int
    timestamp: str
    x: float
    y: float
    heading: float

@router.post("/insert_sample")
async def insert_sample_telemetry(data: TelemetryData):
    telemetry_data = {
        "turtleBotId": data.turtleBotId,
        "timestamp": data.timestamp,
        "x": data.x,
        "y": data.y,
        "heading": data.heading,
    }
    await db.telemetry.create(data=telemetry_data)
    return {"message": "Telemetry data inserted"}




