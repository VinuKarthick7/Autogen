"""Bounded sequential AutoGen review team; agents receive context only."""

import os
from typing import Any

from autogen_ext.models.openai import OpenAIChatCompletionClient

from agents.architecture_agent import ArchitectureAgent
from agents.planning_agent import PlanningAgent
from agents.quality_agent import QualityAgent


class RepositoryReviewTeam:
    """Runs exactly three one-pass reviewers, without tools or agent handoffs."""

    def __init__(self) -> None:
        api_key = os.getenv("OPENAI_API_KEY") or os.getenv("AI_REVIEW_API_KEY")
        if not api_key:
            raise RuntimeError("AI review requires OPENAI_API_KEY (offline deterministic review remains available).")
        client_args: dict[str, Any] = {"model": os.getenv("AI_REVIEW_MODEL", "gpt-4o-mini"), "api_key": api_key}
        if base_url := os.getenv("OPENAI_BASE_URL"):
            client_args["base_url"] = base_url
        self._model_client = OpenAIChatCompletionClient(**client_args)
        self._architecture = ArchitectureAgent(self._model_client)
        self._quality = QualityAgent(self._model_client)
        self._planning = PlanningAgent(self._model_client)

    async def run_review(self, context: dict[str, Any]) -> dict[str, Any]:
        architecture = await self._architecture.review(context)
        quality = await self._quality.review(context)
        planning = await self._planning.review(context, architecture, quality)
        return {"architecture": architecture, "quality": quality, "planning": planning}

    async def close(self) -> None:
        await self._model_client.close()
