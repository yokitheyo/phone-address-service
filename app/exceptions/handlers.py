from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.utils.logging import logger

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Ошибка валидации данных: {exc}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )

async def http_exception_handler(request: Request, exc):
    logger.warning(f"HTTP исключение: {exc.detail} (код {exc.status_code})")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Необработанное исключение: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Внутренняя ошибка сервера"},
    )