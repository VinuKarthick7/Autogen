from fastapi import APIRouter, Depends
from typing import List
from core_platform.projects.models import ProjectModel
from core_platform.projects.service import ProjectService

router = APIRouter(prefix="/projects", tags=["projects"])

def get_project_service():
    return ProjectService()

@router.get("", response_model=List[ProjectModel])
async def list_projects(org_id: str, svc: ProjectService = Depends(get_project_service)):
    return svc.list_projects(org_id)
