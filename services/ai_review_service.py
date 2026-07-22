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
        architecture_context = context["architecture"]
        architecture_issues: list[str] = []
        architecture_recommendations: list[str] = []
        evidence: list[str] = []
        large_module = next((item for item in architecture_context["largest_modules"] if item["lines"] >= 250 or item["functions"] >= 20), None)
        large_directory = next((item for item in architecture_context["largest_directories"] if item["files"] >= 30), None)
        hotspot = next((item for item in architecture_context["dependency_hotspots"] if item["fan_in"] >= 5 or item["fan_out"] >= 10), None)
        if large_module:
            fact = f"{large_module['file']} has {large_module['lines']} lines, {large_module['functions']} functions, and {large_module['classes']} classes."
            architecture_issues.append(fact)
            architecture_recommendations.append(f"Split {large_module['file']} into domain-focused modules around its {large_module['functions']} functions.")
            evidence.append(fact)
        if large_directory and len(architecture_issues) < 5:
            fact = f"Directory {large_directory['path']} contains {large_directory['files']} files."
            architecture_issues.append(fact)
            architecture_recommendations.append(f"Review ownership boundaries inside {large_directory['path']} before adding more modules there.")
            evidence.append(fact)
        if hotspot and len(architecture_issues) < 5:
            fact = f"Dependency hotspot {hotspot['module']} has fan-in {hotspot['fan_in']} and fan-out {hotspot['fan_out']}."
            architecture_issues.append(fact)
            if hotspot["fan_out"] >= hotspot["fan_in"]:
                architecture_recommendations.append(f"Move grouped imports from {hotspot['module']} into a dedicated composition or bootstrap module.")
            else:
                architecture_recommendations.append(f"Reduce direct dependencies on {hotspot['module']} by introducing a focused interface at its callers.")
            evidence.append(fact)
        for cycle in architecture_context["circular_imports"][:1]:
            fact = "Circular import path: " + " -> ".join(cycle)
            architecture_issues.append(fact)
            architecture_recommendations.append(f"Break the circular import involving {cycle[0]} with an interface or dependency inversion.")
            evidence.append(fact)
        strengths = [
            f"Scanner analyzed {structure['total_files']} files with {structure['api_routes']} detected API routes.",
            f"Repository has {len(architecture_context['service_boundaries'])} detected architectural layer groups.",
            f"Route-to-module ratio is {architecture_context['route_to_module_ratio']} across {context['repository']['languages']} source languages.",
        ]
        quality_issues = []
        quality_recommendations = []
        test_target = architecture_context["largest_modules"][0]["file"] if architecture_context["largest_modules"] else "the largest scanned module"
        if quality["test_files"] == 0:
            quality_issues.append("No test files were detected.")
            quality_recommendations.append(f"Add focused tests for {test_target}, the largest scanner-visible Python module.")
        if quality["documentation_score"] < 100:
            quality_issues.append("Repository documentation signals are incomplete.")
            quality_recommendations.append("Document setup and architectural boundaries in the repository README or docs directory.")
        if quality["todo_count"]:
            quality_issues.append(f"{quality['todo_count']} TODO markers were detected.")
            quality_recommendations.append(f"Triage the {quality['todo_count']} scanner-detected TODO markers into owned backlog items.")
        if not quality_issues:
            quality_issues.append("No scanner-visible testing, documentation, or TODO gaps were detected.")
        architecture = {"score": max(context["repository"]["health_score"] - 5 * quality["circular_import_count"], 0), "strengths": strengths, "issues": architecture_issues[:5], "recommendations": architecture_recommendations[:5], "evidence": evidence[:5]}
        quality_review = {"score": context["repository"]["health_score"], "strengths": [f"{quality['test_files']} test files and {structure['api_routes']} API routes were detected."], "issues": quality_issues, "recommendations": quality_recommendations}
        planning = {"priority_1": architecture["recommendations"][:2] + quality_review["recommendations"][:1], "priority_2": quality_review["recommendations"][1:2], "priority_3": [], "roadmap": architecture["recommendations"][:2] + quality_review["recommendations"][:2]}
        return {"architecture": architecture, "quality": quality_review, "planning": planning}


ai_review_service = AIReviewService()
