from fastapi import APIRouter
from simulation.organization_memory import OrganizationMemory
from simulation.velocity_engine import VelocityEngine

router = APIRouter(prefix="/simulation", tags=["simulation"])

memory = OrganizationMemory()
velocity_engine = VelocityEngine(memory)

@router.post("/sprints")
async def create_sprint():
    return {"status": "sprint created"}

@router.post("/rfc")
async def create_rfc():
    return {"status": "rfc generated"}

@router.post("/review")
async def review_rfc():
    return {"status": "review complete"}

@router.post("/retrospective")
async def generate_retrospective():
    return {"status": "retrospective generated"}

@router.post("/hiring")
async def recommend_hiring():
    return {"status": "recommendation generated"}

@router.get("/velocity")
async def get_velocity():
    # Example using hardcoded team
    return {"velocity": velocity_engine.compute_velocity("backend-1")}

@router.get("/team-health")
async def get_team_health():
    return {"health": 0.85}

@router.get("/backlog-pressure")
async def get_backlog_pressure():
    return {"pressure": 0.9}

@router.get("/rfcs")
async def get_rfcs():
    return memory.load_history("rfcs")
