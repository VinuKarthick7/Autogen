from fastapi import Request, HTTPException

ROLES = ["Platform Admin", "Organization Owner", "Team Lead", "Engineer", "Viewer"]

def require_role(allowed_roles: list[str]):
    def role_checker(request: Request):
        # MOCKED: Pull user role from request state
        user_role = getattr(request.state, "user_role", "Platform Admin")
        if user_role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return user_role
    return role_checker

def is_platform_admin(request: Request) -> bool:
    return getattr(request.state, "user_role", "Viewer") == "Platform Admin"
