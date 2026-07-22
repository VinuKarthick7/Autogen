"""Single-pass AutoGen engineering roadmap planner."""

import json
from typing import Any

from autogen_agentchat.agents import AssistantAgent


SYSTEM_PROMPT = """You are an engineering manager.
Generate short-term improvements, medium-term refactors, and a long-term roadmap.
Prioritize impact and avoid vague recommendations. Use only supplied repository context and reviews.
Return JSON only with exactly: priority_1 (string array), priority_2 (string array), priority_3 (string array), roadmap (string array)."""


class PlanningAgent:
    def __init__(self, model_client: Any) -> None:
        self._agent = AssistantAgent("planning_reviewer", model_client=model_client, system_message=SYSTEM_PROMPT, max_tool_iterations=1)

    async def review(self, context: dict[str, Any], architecture: dict[str, Any], quality: dict[str, Any]) -> dict[str, Any]:
        task = {"repository_context": context, "architecture_review": architecture, "quality_review": quality}
        result = await self._agent.run(task=json.dumps(task, separators=(',', ':')))
        text = str(result.messages[-1].content).strip().removeprefix("```json").removesuffix("```").strip()
        payload = json.loads(text)
        return {key: list(payload[key]) for key in ("priority_1", "priority_2", "priority_3", "roadmap")}
