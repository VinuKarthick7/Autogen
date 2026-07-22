from fastapi import Request
from fastapi.responses import JSONResponse
from api.schemas.api_error import ApiError

async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=ApiError(detail=str(exc), code="INTERNAL_SERVER_ERROR").model_dump()
    )
