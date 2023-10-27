from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings
from app.db.db_init import create_table

if settings.TABLE_ISNT_EXIST:
    # 테이블이 생성되어 있지 않은 경우 생성 필요
    create_table()

app = FastAPI(title="ComMoni")

app.include_router(router=api_router, prefix=settings.API_PREFIX_ENDPOINT)
