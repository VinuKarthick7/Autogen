from core_platform.organizations.models import OrganizationModel, TeamModel
import uuid

# Mock Database
MOCK_ORGS = {
    "org_1": OrganizationModel(
        org_id="org_1",
        name="Acme Corp",
        billing_plan="Enterprise",
        teams=[
            TeamModel(team_id="t_1", name="PMS Team", members=["alice@acme.com", "bob@acme.com"]),
            TeamModel(team_id="t_2", name="ERP Team", members=["charlie@acme.com"]),
            TeamModel(team_id="t_3", name="E-commerce Team", members=["dave@acme.com"])
        ]
    )
}

class OrganizationService:
    def get_organization(self, org_id: str) -> OrganizationModel:
        if org_id in MOCK_ORGS:
            return MOCK_ORGS[org_id]
        raise ValueError("Organization not found")

    def list_organizations(self) -> list[OrganizationModel]:
        return list(MOCK_ORGS.values())

    def create_organization(self, name: str, billing_plan: str = "Free") -> OrganizationModel:
        org_id = f"org_{uuid.uuid4().hex[:8]}"
        org = OrganizationModel(org_id=org_id, name=name, billing_plan=billing_plan, teams=[])
        MOCK_ORGS[org_id] = org
        return org
