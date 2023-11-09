from fastapi import Request
from fastapi.responses import JSONResponse

from app.exception.api_exception import APIExceptionBase


def base_exception_handler(_: Request, exc: APIExceptionBase):
    return JSONResponse(status_code=exc.status,
                        content=exc.make_content())
