from fastapi import Request
from fastapi.responses import JSONResponse

from app.exception.api_exception import APIExceptionBase


def base_exception_handler(_: Request, exc: APIExceptionBase):
    if exc.headers:
        return JSONResponse(status_code=exc.http_status,
                            headers=exc.headers,
                            content=exc.make_content())
    else:
        return JSONResponse(status_code=exc.http_status,
                            content=exc.make_content())
