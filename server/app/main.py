from typing import Union

from fastapi import FastAPI

from server.app.api.router import api_router
from server.app.core.config import settings

app = FastAPI(title="ComMoni")

app.include_router(router=api_router, prefix=settings.API_PREFIX_ENDPOINT)
