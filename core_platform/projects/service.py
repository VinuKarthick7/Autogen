from core_platform.projects.models import ProjectModel

MOCK_PROJECTS = {
    "proj_1": ProjectModel(project_id="proj_1", org_id="org_1", name="Core Banking", repositories=["pms", "erp"]),
    "proj_2": ProjectModel(project_id="proj_2", org_id="org_1", name="Web Shop", repositories=["ecommerce"])
}

class ProjectService:
    def list_projects(self, org_id: str) -> list[ProjectModel]:
        return [p for p in MOCK_PROJECTS.values() if p.org_id == org_id]
