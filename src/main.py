from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.exceptions import AppException
from src.logs import setup_logging


app = FastAPI()

setup_logging()

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )
