# src/api/routes/lidar.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.database import db, connect_db

router = APIRouter()

class LidarCreate(BaseModel):
    turtleBotId: int
    timestamp: str
    ranges: list

@router.post("/lidar", tags=["turtlebot3"])
async def insert_sample_lidar(lidar: LidarCreate):
    await connect_db()
    try:
        await db.lidar.create({
            "turtleBotId": lidar.turtleBotId,
            "timestamp": lidar.timestamp,
            "ranges": lidar.ranges,
        })
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to insert lidar: {str(e)}")

@router.get("/lidar", tags=["turtlebot3"])
async def get_latest_lidar():
    await connect_db()
    try:
        lidar = await db.lidar.find_first(order={"timestamp": "desc"})
        return {"data": lidar}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch lidar: {str(e)}")
