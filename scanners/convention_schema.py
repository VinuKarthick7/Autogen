from typing import List, Optional

from pydantic import BaseModel


class ProjectInfo(BaseModel):
    name: str
    backend_framework: str
    frontend_framework: str
    database: str


class FolderStructure(BaseModel):
    routers_path: Optional[str] = None
    models_path: Optional[str] = None
    services_path: Optional[str] = None
    schemas_path: Optional[str] = None
    screens_path: Optional[str] = None
    widgets_path: Optional[str] = None


class DatabaseConvention(BaseModel):
    base_model_name: Optional[str] = None
    common_fields: List[str] = []
    timestamp_fields: List[str] = []
    tenant_field: Optional[str] = None
    migration_tool: Optional[str] = None


class AuthConvention(BaseModel):
    auth_type: Optional[str] = None
    dependency_name: Optional[str] = None
    role_checker: Optional[str] = None


class ApiConvention(BaseModel):
    response_envelope: List[str] = []
    pagination_style: Optional[str] = None
    error_format: Optional[str] = None


class FrontendConvention(BaseModel):
    state_management: Optional[str] = None
    navigation: Optional[str] = None
    architecture_pattern: Optional[str] = None


class ExistingModules(BaseModel):
    modules: List[str] = []


class ConventionSchema(BaseModel):
    project_info: ProjectInfo

    folder_structure: FolderStructure

    database: DatabaseConvention

    auth: AuthConvention

    api: ApiConvention

    frontend: FrontendConvention

    existing_modules: ExistingModules