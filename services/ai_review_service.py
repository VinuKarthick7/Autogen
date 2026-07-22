"""Cached AI repository review orchestration built on scanner output."""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import Any

from agents.review_team import RepositoryReviewTeam
from services.repository_context_builder import RepositoryContextBuilder
from services.repository_scanner import repository_scanner


class AIReviewService:
    def __init__(self) -> None:
        self._builder = RepositoryContextBuilder()
        self._cache: dict[tuple[str, str], dict[str, Any]] = {}
        self._lock = asyncio.Lock()

    async def review_repository(self, repository_path: str) -> dict[str, Any]:
        scanner_result = repository_scanner.analyze(repository_path)
        cache_key = (scanner_result["path"], scanner_result["scanned_at"])
        async with self._lock:
            if cache_key in self._cache:
                return {**self._cache[cache_key], "cached": True}
        context = self._builder.build(scanner_result)
        review, mode = await self._run_review(context)
        result = {"repository": context["repository"], **review, "generated_at": datetime.now(timezone.utc).isoformat(), "review_mode": mode, "context": context, "cached": False}
        async with self._lock:
            self._cache[cache_key] = result
        return result

    async def _run_review(self, context: dict[str, Any]) -> tuple[dict[str, Any], str]:
        try:
            team = RepositoryReviewTeam()
        except RuntimeError:
            return self._offline_review(context), "offline-deterministic"
        try:
            return await team.run_review(context), "autogen"
        finally:
            await team.close()

    @staticmethod
    def _offline_review(context: dict[str, Any]) -> dict[str, Any]:
        """Offline reasoning from scanner facts only; never reads repository files."""
        quality = context["quality"]
        structure = context["structure"]
        dependencies = context["dependencies"]
        architecture_issues = []
        architecture_recommendations = []
        if quality["circular_imports"]:
            architecture_issues.append(f"{quality['circular_imports']} circular import relationships were detected.")
            architecture_recommendations.append("Break circular dependency paths behind a stable interface.")
        if not structure["directories"]:
            architecture_issues.append("Scanner output contains limited module-structure evidence.")
        if not architecture_issues:
            architecture_issues.append("No circular imports were detected in the scanner dependency graph.")
        quality_issues = []
        quality_recommendations = []
        if quality["test_files"] == 0:
            quality_issues.append("No test files were detected.")
            quality_recommendations.append("Add focused tests around the highest-risk modules first.")
        if quality["documentation_score"] < 100:
            quality_issues.append("Repository documentation signals are incomplete.")
            quality_recommendations.append("Document setup, boundaries, and operational workflows in the README or docs directory.")
        if quality["todo_count"]:
            quality_issues.append(f"{quality['todo_count']} TODO markers were detected.")
            quality_recommendations.append("Triage TODO markers into owned, dated backlog items.")
        if not quality_issues:
            quality_issues.append("No scanner-visible testing, documentation, or TODO gaps were detected.")
        architecture = {"score": max(context["repository"]["health_score"] - 5 * quality["circular_imports"], 0), "strengths": [f"{structure['total_files']} files were analyzed deterministically.", f"{len(dependencies['internal_imports'])} internal import signals are available for review."], "issues": architecture_issues, "recommendations": architecture_recommendations or ["Keep module boundaries explicit as the repository grows."]}
        quality_review = {"score": context["repository"]["health_score"], "strengths": [f"{quality['test_files']} test files and {structure['api_routes']} API routes were detected."], "issues": quality_issues, "recommendations": quality_recommendations or ["Maintain the current testing and documentation signals."]}
        planning = {"priority_1": architecture["recommendations"][:1] + quality_review["recommendations"][:1], "priority_2": quality_review["recommendations"][1:2], "priority_3": ["Review dependency hotspots before the next major feature boundary."], "roadmap": ["Immediate: address priority-1 scanner-evidenced risks.", "Next sprint: strengthen tests and documentation around hotspot modules.", "Long term: track architectural health on each repository scan."]}
        return {"architecture": architecture, "quality": quality_review, "planning": planning}


ai_review_service = AIReviewService()
