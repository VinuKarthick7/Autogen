from fastapi import APIRouter

router = APIRouter(prefix="/repairs", tags=["repairs"])

@router.get("")
async def list_repairs():
    return []
