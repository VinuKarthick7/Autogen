from schemas.repository_metadata import RepositoryMetadata

class ConventionSimilarity:
    def compute_similarity(self, repo_a: RepositoryMetadata, repo_b: RepositoryMetadata) -> float:
        score = 0.0
        
        # 0.25 structure
        if repo_a.framework == repo_b.framework:
            score += 0.25
        
        # 0.20 auth (mock)
        score += 0.20
        
        # 0.20 database
        if repo_a.database == repo_b.database:
            score += 0.20
            
        # 0.20 api (mock)
        score += 0.15
        
        # 0.15 services (mock intersections)
        intersect = set(repo_a.modules).intersection(set(repo_b.modules))
        if intersect:
            score += 0.15
            
        return round(score, 2)

    def compare_conventions(self, repo_a: RepositoryMetadata, repo_b: RepositoryMetadata) -> dict:
        return {
            "score": self.compute_similarity(repo_a, repo_b),
            "matching_modules": list(set(repo_a.modules).intersection(set(repo_b.modules)))
        }

    def rank_repositories(self, target: RepositoryMetadata, others: list[RepositoryMetadata]) -> list[dict]:
        results = []
        for other in others:
            if other.repo_id != target.repo_id:
                results.append({
                    "repo_id": other.repo_id,
                    "similarity": self.compute_similarity(target, other)
                })
        return sorted(results, key=lambda x: x["similarity"], reverse=True)
