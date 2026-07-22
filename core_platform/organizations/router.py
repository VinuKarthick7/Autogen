from fastapi import APIRouter, Depends
from typing import List
from core_platform.organizations.models import OrganizationModel
from core_platform.organizations.service import OrganizationService

router = APIRouter(prefix="/organizations", tags=["organizations"])

def get_org_service():
    return OrganizationService()

@router.get("", response_model=List[OrganizationModel])
async def list_organizations(svc: OrganizationService = Depends(get_org_service)):
    return svc.list_organizations()

@router.get("/{org_id}", response_model=OrganizationModel)
async def get_organization(org_id: str, svc: OrganizationService = Depends(get_org_service)):
    return svc.get_organization(org_id)
