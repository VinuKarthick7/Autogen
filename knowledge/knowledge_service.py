from knowledge.repository_registry import RepositoryRegistry
from knowledge.global_symbol_index import GlobalSymbolIndex
from knowledge.cross_repo_graph import CrossRepoGraph
from knowledge.pattern_extractor import PatternExtractor
from knowledge.repair_recommender import RepairRecommender

class KnowledgeService:
    def __init__(self):
        self.registry = RepositoryRegistry()
        self.symbol_index = GlobalSymbolIndex()
        self.graph = CrossRepoGraph()
        self.pattern_extractor = PatternExtractor()
        self.repair_recommender = RepairRecommender()

    def get_repositories(self):
        return self.registry.list_repositories()

    def get_repository(self, repo_id: str):
        return self.registry.get_repository(repo_id)

    def search_symbols(self, query: str):
        return self.symbol_index.search(query)

    def get_graph(self):
        return self.graph.export_graph()

    def get_patterns(self):
        # mock list
        return [{"pattern": "Coupon pattern", "repo": "pms"}]

    def get_repairs(self):
        return [h.model_dump() for h in self.repair_recommender.history]
