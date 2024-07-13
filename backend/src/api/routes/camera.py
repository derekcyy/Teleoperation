# src/api/routes/camera.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.database import db, connect_db

router = APIRouter()

class CameraCreate(BaseModel):
    turtleBotId: int
    timestamp: str
    image: bytes

@router.post("/camera", tags=["turtlebot3"])
async def insert_sample_camera(camera: CameraCreate):
    await connect_db()
    try:
        await db.camera.create({
            "turtleBotId": camera.turtleBotId,
            "timestamp": camera.timestamp,
            "image": camera.image,
        })
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to insert camera: {str(e)}")

@router.get("/camera", tags=["turtlebot3"])
async def get_latest_camera():
    await connect_db()
    try:
        camera = await db.camera.find_first(order={"timestamp": "desc"})
        return {"data": camera}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch camera: {str(e)}")
