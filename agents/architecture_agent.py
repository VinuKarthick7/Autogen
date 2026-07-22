"""Single-pass AutoGen architecture reviewer."""

import json
from typing import Any

from autogen_agentchat.agents import AssistantAgent


SYSTEM_PROMPT = """You are a principal software architect reviewing a production codebase.
Evaluate modularity, separation of concerns, dependency direction, scalability, and maintainability.
Provide concise engineering feedback. Do not hallucinate. Use only supplied repository context.
Return JSON only with exactly: score (0-100), strengths (string array), issues (string array), recommendations (string array)."""


class ArchitectureAgent:
    def __init__(self, model_client: Any) -> None:
        self._agent = AssistantAgent("architecture_reviewer", model_client=model_client, system_message=SYSTEM_PROMPT, max_tool_iterations=1)

    async def review(self, context: dict[str, Any]) -> dict[str, Any]:
        result = await self._agent.run(task=f"Repository context:\n{json.dumps(context, separators=(',', ':'))}")
        return _json_response(result.messages[-1].content)


def _json_response(content: Any) -> dict[str, Any]:
    text = str(content).strip().removeprefix("```json").removesuffix("```").strip()
    payload = json.loads(text)
    return {"score": int(payload["score"]), "strengths": list(payload["strengths"]), "issues": list(payload["issues"]), "recommendations": list(payload["recommendations"])}
