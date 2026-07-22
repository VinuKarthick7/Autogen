"""Single-pass AutoGen quality reviewer."""

import json
from typing import Any

from autogen_agentchat.agents import AssistantAgent

from agents.architecture_agent import _json_response


SYSTEM_PROMPT = """You are a senior engineering quality reviewer.
Review code quality, maintainability, testing, documentation, and technical debt.
Do not invent facts. Use only supplied repository context.
Return JSON only with exactly: score (0-100), strengths (string array), issues (string array), recommendations (string array)."""


class QualityAgent:
    def __init__(self, model_client: Any) -> None:
        self._agent = AssistantAgent("quality_reviewer", model_client=model_client, system_message=SYSTEM_PROMPT, max_tool_iterations=1)

    async def review(self, context: dict[str, Any]) -> dict[str, Any]:
        result = await self._agent.run(task=f"Repository context:\n{json.dumps(context, separators=(',', ':'))}")
        return _json_response(result.messages[-1].content)
