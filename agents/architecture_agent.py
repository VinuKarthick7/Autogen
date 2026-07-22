"""Single-pass AutoGen architecture reviewer."""

import json
from typing import Any

from autogen_agentchat.agents import AssistantAgent


SYSTEM_PROMPT = """You are a principal software architect reviewing a production repository.

You may ONLY use the supplied repository context.

Evaluate:
- modularity
- layering
- dependency direction
- cohesion
- coupling
- scalability
- maintainability

Rules:
1. Every issue must reference concrete repository evidence.
2. Every recommendation must reference a specific module, directory, metric, or dependency hotspot.
3. Do not give generic advice.
4. Do not invent missing information.
5. Positive findings belong in strengths.
6. Missing problems are not issues.
7. Provide at least 3 strengths, at most 5 issues, and at most 5 recommendations.
8. Every issue needs a matching evidence entry.

Bad examples:
- Improve architecture.
- Refactor modules.
- Keep boundaries explicit.

Good examples:
- booking/service.py contains 42 functions and should be split into smaller domain services.
- app/modules contains 143 files and may become difficult to maintain.
- core/config is imported by 47 modules and is a dependency hotspot.

Return JSON only with exactly: score (0-100), strengths (string array), issues (string array), recommendations (string array), evidence (string array)."""


class ArchitectureAgent:
    def __init__(self, model_client: Any) -> None:
        self._agent = AssistantAgent("architecture_reviewer", model_client=model_client, system_message=SYSTEM_PROMPT, max_tool_iterations=1)

    async def review(self, context: dict[str, Any]) -> dict[str, Any]:
        result = await self._agent.run(task=f"Repository context:\n{json.dumps(context, separators=(',', ':'))}")
        review = _json_response(result.messages[-1].content)
        evidence_tokens = _evidence_tokens(context)
        review["issues"] = [item for item in review["issues"] if _references_evidence(item, evidence_tokens)]
        review["recommendations"] = [item for item in review["recommendations"] if _references_evidence(item, evidence_tokens)]
        review["evidence"] = [item for item in review["evidence"] if _references_evidence(item, evidence_tokens)]
        return review


def _json_response(content: Any) -> dict[str, Any]:
    text = str(content).strip().removeprefix("```json").removesuffix("```").strip()
    payload = json.loads(text)
    return {"score": int(payload["score"]), "strengths": list(payload["strengths"])[:8], "issues": list(payload["issues"])[:5], "recommendations": list(payload["recommendations"])[:5], "evidence": list(payload.get("evidence", []))[:5]}


def _evidence_tokens(context: dict[str, Any]) -> set[str]:
    architecture = context["architecture"]
    tokens = {str(item["file"]).lower() for item in architecture["largest_modules"]}
    tokens.update(str(item["path"]).lower() for item in architecture["largest_directories"])
    tokens.update(str(item["module"]).lower() for item in architecture["dependency_hotspots"])
    tokens.update(str(item["prefix"]).lower() for item in architecture["api_groups"])
    return {token for token in tokens if len(token) > 1}


def _references_evidence(text: str, tokens: set[str]) -> bool:
    lowered = text.lower()
    return any(token in lowered for token in tokens)
