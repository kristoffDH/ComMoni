from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.exception.api_exception import APIExceptionBase
from app.exception.exception_handler import base_exception_handler

app = FastAPI(title="ComMoni")

app.include_router(router=api_router, prefix=settings.API_PREFIX_ENDPOINT)

app.add_exception_handler(APIExceptionBase, base_exception_handler)
