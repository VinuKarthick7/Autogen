from fastapi import APIRouter, Depends
from evolution.evolution_service import EvolutionService

router = APIRouter(prefix="/evolution", tags=["evolution"])

def get_evolution_service():
    return EvolutionService()

@router.get("/recommendations")
async def get_recommendations(svc: EvolutionService = Depends(get_evolution_service)):
    return svc.get_recommendations()

@router.get("/strategies")
async def get_strategies(svc: EvolutionService = Depends(get_evolution_service)):
    return svc.get_strategy_rankings()

@router.get("/prompts")
async def get_prompts(svc: EvolutionService = Depends(get_evolution_service)):
    return svc.get_prompt_history()

@router.get("/experiments")
async def get_experiments(svc: EvolutionService = Depends(get_evolution_service)):
    return svc.get_experiments()

@router.post("/experiments")
async def create_experiment():
    return {"status": "created"}

@router.post("/learning-cycle")
async def trigger_learning_cycle(svc: EvolutionService = Depends(get_evolution_service)):
    return svc.trigger_learning_cycle()
