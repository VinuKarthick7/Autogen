from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from api.services.artifact_service import ArtifactService

router = APIRouter(prefix="/runs/{run_id}", tags=["artifacts"])

def get_artifact_service():
    return ArtifactService()

@router.get("/artifacts")
async def get_artifacts(run_id: str, svc: ArtifactService = Depends(get_artifact_service)):
    # Returns links or list of artifacts
    return {"message": "Use specific endpoints for artifacts"}

@router.get("/plan")
async def get_plan(run_id: str, svc: ArtifactService = Depends(get_artifact_service)):
    return svc.load_plan(run_id)
    
@router.get("/patch")
async def get_patch(run_id: str, svc: ArtifactService = Depends(get_artifact_service)):
    return svc.load_patch(run_id)
    
@router.get("/verification")
async def get_verification(run_id: str, svc: ArtifactService = Depends(get_artifact_service)):
    return svc.load_verification(run_id)
    
@router.get("/chat")
async def get_chat(run_id: str, svc: ArtifactService = Depends(get_artifact_service)):
    return svc.load_chat(run_id)

@router.get("/dependency-graph")
async def get_graph(run_id: str, svc: ArtifactService = Depends(get_artifact_service)):
    return svc.load_graph(run_id)
    
@router.get("/repair-history")
async def get_repair_history(run_id: str, svc: ArtifactService = Depends(get_artifact_service)):
    return {"message": "Not implemented"}
