from fastapi import APIRouter, Depends
from typing import List
from api.schemas.create_run import CreateRunRequest
from api.schemas.run_status import RunStatus
from api.services.workflow_service import WorkflowService

router = APIRouter(prefix="/runs", tags=["runs"])

def get_workflow_service():
    return WorkflowService()

@router.post("", response_model=RunStatus)
async def create_run(request: CreateRunRequest, svc: WorkflowService = Depends(get_workflow_service)):
    return await svc.start_workflow(request)

@router.get("", response_model=List[RunStatus])
async def list_runs(svc: WorkflowService = Depends(get_workflow_service)):
    return await svc.list_runs()

@router.get("/{run_id}", response_model=RunStatus)
async def get_run(run_id: str, svc: WorkflowService = Depends(get_workflow_service)):
    return await svc.get_status(run_id)

@router.delete("/{run_id}")
async def cancel_run(run_id: str, svc: WorkflowService = Depends(get_workflow_service)):
    await svc.cancel_workflow(run_id)
    return {"status": "cancelled"}
