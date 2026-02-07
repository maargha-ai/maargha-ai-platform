import uuid
from fastapi import Request
from app.core.logger import logger

async def logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    logger.info(
        "request_started",
        method=request.method,
        path=request.url.path,
        request_id=request_id,
    )

    response = await call_next(request)

    logger.info(
        "request_completed",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        request_id=request_id,
    )
    return response
