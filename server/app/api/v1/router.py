from fastapi import APIRouter

from app.api.v1.endpoints import cominfo_api
from app.api.v1.endpoints import commanage_api

from app.core.config import settings

api_router = APIRouter()

api_router.include_router(cominfo_api.router, prefix=f"{settings.API_VERSION}/commoni", tags=["commoni"])
api_router.include_router(commanage_api.router, prefix=f"{settings.API_VERSION}/commanage", tags=["commanage"])
