"""Build a compact, scanner-only context for repository review agents."""

from __future__ import annotations

from collections import Counter
from typing import Any


class RepositoryContextBuilder:
    """Converts deterministic scanner output into a bounded review payload."""

    def build(self, scanner_result: dict[str, Any]) -> dict[str, Any]:
        edges = scanner_result.get("dependency_edges", [])[:80]
        modules = Counter(edge["source"] for edge in edges)
        directories = sorted({route["module"].split(".")[0] for route in scanner_result.get("api_routes", []) if route.get("module")})[:20]
        import_groups = scanner_result.get("imports_by_category", {})
        return {
            "repository": {"name": scanner_result["repository_name"], "path": scanner_result["path"], "tech_stack": self._tech_stack(scanner_result), "languages": list(scanner_result.get("source_languages", {}).keys())[:12], "health_score": scanner_result["health_score"]},
            "structure": {"total_files": scanner_result["files"], "directories": directories, "largest_modules": [{"module": name, "dependency_references": count} for name, count in modules.most_common(12)], "api_routes": scanner_result["api_endpoints"], "database_models": scanner_result["database_models"]},
            "quality": {"test_files": scanner_result["tests"], "todo_count": scanner_result.get("todos", 0), "documentation_score": self._documentation_score(scanner_result), "circular_imports": scanner_result.get("circular_imports", 0)},
            "dependencies": {"internal_imports": import_groups.get("Internal project imports", [])[:12], "external_imports": import_groups.get("Third-party packages", [])[:12], "hotspots": [{"module": name, "dependency_references": count} for name, count in modules.most_common(8)]},
        }

    @staticmethod
    def _tech_stack(result: dict[str, Any]) -> list[str]:
        packages = [item["module"].split(".")[0] for item in result.get("imports_by_category", {}).get("Third-party packages", [])]
        return list(dict.fromkeys(packages))[:12]

    @staticmethod
    def _documentation_score(result: dict[str, Any]) -> int:
        checks = {item["Signal"]: item["Status"] for item in result.get("health_checks", [])}
        return 100 if checks.get("Documentation") == "Pass" and checks.get("Meaningful README") == "Pass" else 50 if checks.get("Meaningful README") == "Pass" else 0
