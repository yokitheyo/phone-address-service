from fastapi import FastAPI, Request, Depends, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.config.config import settings
from app.routers.routers import router, get_redis_service
from app.services.services import RedisService
from app.utils.logging import logger, setup_logging
from app.exceptions.handlers import validation_exception_handler, http_exception_handler, global_exception_handler
import time

setup_logging()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="RESTful сервис для хранения и получения адресов по номеру телефона"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.4f}s")
    return response

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

@app.get("/health", response_model=dict, summary="Проверка работоспособности сервиса", tags=["Health"])
async def health_check(redis_service: RedisService = Depends(get_redis_service)):
    redis_status = await redis_service.ping()
    
    if not redis_status:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "unhealthy", "redis": "unavailable"}
        )
    
    return {"status": "healthy", "redis": "available"}

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)