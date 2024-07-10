# src/api/routes/__init__.py
from fastapi import APIRouter
from .telemetry import router as telemetry_router
from .battery import router as battery_router
from .camera import router as camera_router
from .lidar import router as lidar_router
from .waypoint import router as waypoint_router

api_router = APIRouter()
api_router.include_router(telemetry_router, prefix="/api/telemetry")
api_router.include_router(battery_router, prefix="/battery")
api_router.include_router(camera_router, prefix="/camera")
api_router.include_router(lidar_router, prefix="/lidar")
api_router.include_router(waypoint_router, prefix="/waypoint")
