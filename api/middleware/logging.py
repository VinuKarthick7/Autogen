import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api.request")

async def log_request_middleware(request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response
