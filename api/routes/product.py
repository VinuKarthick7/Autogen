from fastapi import APIRouter

router = APIRouter(prefix="/product", tags=["product"])

@router.post("/prd")
async def upload_prd():
    return {"status": "prd parsed"}

@router.post("/epics")
async def generate_epics():
    return {"status": "epics generated"}

@router.post("/stories")
async def generate_stories():
    return {"status": "stories generated"}

@router.post("/roadmap")
async def generate_roadmap():
    return {"status": "roadmap generated"}

@router.post("/sprints")
async def generate_sprints():
    return {"status": "sprints generated"}

@router.get("/requirements")
async def get_requirements():
    return []

@router.get("/roadmaps")
async def get_roadmaps():
    return []

@router.get("/releases")
async def get_releases():
    return []
