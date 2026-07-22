from fastapi import APIRouter, Depends
from api.schemas.benchmark_request import BenchmarkRequest
from api.services.benchmark_service import BenchmarkService

router = APIRouter(prefix="/benchmarks", tags=["benchmarks"])

def get_benchmark_service():
    return BenchmarkService()

@router.post("/run")
async def run_benchmark(req: BenchmarkRequest, svc: BenchmarkService = Depends(get_benchmark_service)):
    return await svc.run_suite(req.suite, req.difficulty)
    
@router.get("/results")
async def get_results(suite_run_id: str, svc: BenchmarkService = Depends(get_benchmark_service)):
    return svc.get_results(suite_run_id)
    
@router.get("/leaderboard")
async def get_leaderboard(svc: BenchmarkService = Depends(get_benchmark_service)):
    return svc.get_leaderboard()
