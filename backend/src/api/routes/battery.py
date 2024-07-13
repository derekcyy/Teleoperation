# src/api/routes/battery.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.database import db, connect_db

router = APIRouter()

class BatteryCreate(BaseModel):
    turtleBotId: int
    timestamp: str
    voltage: float
    current: float
    percentage: float

@router.post("/battery", tags=["turtlebot3"])
async def insert_sample_battery(battery: BatteryCreate):
    await connect_db()
    try:
        await db.battery.create({
            "turtleBotId": battery.turtleBotId,
            "timestamp": battery.timestamp,
            "voltage": battery.voltage,
            "current": battery.current,
            "percentage": battery.percentage,
        })
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to insert battery: {str(e)}")

@router.get("/battery", tags=["turtlebot3"])
async def get_latest_battery():
    await connect_db()
    try:
        battery = await db.battery.find_first(order={"timestamp": "desc"})
        return {"data": battery}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch battery: {str(e)}")
