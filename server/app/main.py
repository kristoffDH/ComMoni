from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.db.db_init import create_table

app = FastAPI(title="ComMoni")

app.include_router(router=api_router, prefix=settings.API_PREFIX_ENDPOINT)
