from fastapi import APIRouter, Depends
from api.schemas.approval_request import ApprovalRequest
from api.schemas.run_status import RunStatus
from api.services.approval_service import ApprovalService

router = APIRouter(prefix="/runs/{run_id}", tags=["approvals"])

def get_approval_service():
    return ApprovalService()

@router.post("/approve", response_model=RunStatus)
async def approve(run_id: str, req: ApprovalRequest, svc: ApprovalService = Depends(get_approval_service)):
    return await svc.approve(run_id, req.notes)

@router.post("/reject", response_model=RunStatus)
async def reject(run_id: str, req: ApprovalRequest, svc: ApprovalService = Depends(get_approval_service)):
    return await svc.reject(run_id, req.notes)
