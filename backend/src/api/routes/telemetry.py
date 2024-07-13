# src/api/routes/telemetry.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.database import db, connect_db

router = APIRouter()

class TelemetryCreate(BaseModel):
    turtleBotId: int
    timestamp: str
    x: float
    y: float
    heading: float

@router.post("/telemetry", tags=["turtlebot3"])
async def insert_sample_telemetry(telemetry: TelemetryCreate):
    await connect_db()
    try:
        await db.telemetry.create({
            "turtleBotId": telemetry.turtleBotId,
            "timestamp": telemetry.timestamp,
            "x": telemetry.x,
            "y": telemetry.y,
            "heading": telemetry.heading,
        })
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to insert telemetry: {str(e)}")

@router.get("/telemetry", tags=["turtlebot3"])
async def get_latest_telemetry():
    await connect_db()
    try:
        telemetry = await db.telemetry.find_first(order={"timestamp": "desc"})
        return {"data": telemetry}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch telemetry: {str(e)}")
