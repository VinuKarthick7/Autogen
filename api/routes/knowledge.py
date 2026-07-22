from fastapi import APIRouter, Depends
from schemas.repository_metadata import RepositoryMetadata
from knowledge.knowledge_service import KnowledgeService

router = APIRouter(prefix="/knowledge", tags=["knowledge"])

def get_knowledge_service():
    return KnowledgeService()

@router.post("/repositories")
async def register_repository(metadata: RepositoryMetadata, svc: KnowledgeService = Depends(get_knowledge_service)):
    svc.registry.register_repository(metadata)
    return {"status": "registered"}

@router.get("/repositories")
async def list_repositories(svc: KnowledgeService = Depends(get_knowledge_service)):
    return svc.get_repositories()

@router.get("/repositories/{repo_id}")
async def get_repository(repo_id: str, svc: KnowledgeService = Depends(get_knowledge_service)):
    return svc.get_repository(repo_id)

@router.get("/search")
async def search_symbols(query: str, svc: KnowledgeService = Depends(get_knowledge_service)):
    return svc.search_symbols(query)

@router.get("/similar/{repo_id}")
async def get_similar_repos(repo_id: str, svc: KnowledgeService = Depends(get_knowledge_service)):
    return svc.graph.find_similar_repositories(repo_id)

@router.get("/patterns")
async def get_patterns(svc: KnowledgeService = Depends(get_knowledge_service)):
    return svc.get_patterns()

@router.get("/repairs")
async def get_repairs(svc: KnowledgeService = Depends(get_knowledge_service)):
    return svc.get_repairs()

@router.get("/graph")
async def get_graph(svc: KnowledgeService = Depends(get_knowledge_service)):
    return svc.get_graph()
