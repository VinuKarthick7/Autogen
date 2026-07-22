class RepositoryService:
    def sync_repository(self, provider: str, url: str):
        if provider == "github":
            from .github import sync_github_repo
            return sync_github_repo(url)
        elif provider == "gitlab":
            from .gitlab import sync_gitlab_repo
            return sync_gitlab_repo(url)
        else:
            raise ValueError("Unsupported provider")
