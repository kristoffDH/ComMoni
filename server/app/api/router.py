from fastapi import APIRouter

from server.app.api.endpoints import cpu
from server.app.api.endpoints import disk
from server.app.api.endpoints import memory
from server.app.api.endpoints import network

api_router = APIRouter()
api_router.include_router(cpu.router, prefix="/cpu", tags=["cpu"])
api_router.include_router(disk.router, prefix="/disk", tags=["disk"])
api_router.include_router(memory.router, prefix="/memory", tags=["memory"])
api_router.include_router(network.router, prefix="/network", tags=["network"])
