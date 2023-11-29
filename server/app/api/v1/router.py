from fastapi import APIRouter

from app.api.v1.endpoints import cominfo_api
from app.api.v1.endpoints import commanage_api
from app.api.v1.endpoints import user_api
from app.api.v1.endpoints import login_api

api_v1_router = APIRouter()

api_v1_router.include_router(cominfo_api.router, prefix="/cominfo", tags=["cominfo"])
api_v1_router.include_router(commanage_api.router, prefix="/commanage", tags=["commanage"])
api_v1_router.include_router(user_api.router, prefix="/user", tags=["user"])
api_v1_router.include_router(login_api.router, prefix="/login", tags=["login"])
