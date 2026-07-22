"""Single-pass AutoGen engineering roadmap planner."""

import json
from typing import Any

from autogen_agentchat.agents import AssistantAgent


SYSTEM_PROMPT = """You are an engineering manager.
Generate short-term improvements, medium-term refactors, and a long-term roadmap from the supplied context and reviews only.

Every roadmap item must cite a concrete module, directory, API group, dependency hotspot, or measured gap from the architecture evidence. Do not use generic recommendations or invent facts.

Bad examples:
- Improve documentation.
- Refactor architecture.

Good examples:
- Split booking/service.py during Sprint 2.
- Reduce dependencies on core/config.
- Create repository interfaces for payment modules.

Return JSON only with exactly: priority_1 (string array), priority_2 (string array), priority_3 (string array), roadmap (string array)."""


class PlanningAgent:
    def __init__(self, model_client: Any) -> None:
        self._agent = AssistantAgent("planning_reviewer", model_client=model_client, system_message=SYSTEM_PROMPT, max_tool_iterations=1)

    async def review(self, context: dict[str, Any], architecture: dict[str, Any], quality: dict[str, Any]) -> dict[str, Any]:
        task = {"repository_context": context, "architecture_review": architecture, "quality_review": quality}
        result = await self._agent.run(task=json.dumps(task, separators=(',', ':')))
        text = str(result.messages[-1].content).strip().removeprefix("```json").removesuffix("```").strip()
        payload = json.loads(text)
        tokens = self._evidence_tokens(context)
        return {key: [item for item in list(payload[key]) if self._references_evidence(item, tokens)] for key in ("priority_1", "priority_2", "priority_3", "roadmap")}

    @staticmethod
    def _evidence_tokens(context: dict[str, Any]) -> set[str]:
        architecture = context["architecture"]
        tokens = {str(item["file"]).lower() for item in architecture["largest_modules"]}
        tokens.update(str(item["path"]).lower() for item in architecture["largest_directories"])
        tokens.update(str(item["module"]).lower() for item in architecture["dependency_hotspots"])
        tokens.update(str(item["prefix"]).lower() for item in architecture["api_groups"])
        return {token for token in tokens if len(token) > 1}

    @staticmethod
    def _references_evidence(text: str, tokens: set[str]) -> bool:
        return any(token in str(text).lower() for token in tokens)
