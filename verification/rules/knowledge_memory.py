import os
import yaml
from typing import List
from schemas.patch_set import PatchSet
from schemas.rule_violation import RuleViolation
from orchestrator.gemini_client import GeminiClient
import asyncio
from autogen_core.models import UserMessage, SystemMessage

class KnowledgeMemoryEngine:
    def __init__(self, knowledge_dir: str = "knowledge"):
        self.knowledge_dir = knowledge_dir
        self.regressions = self._load_yaml("regressions.yaml").get("regressions", [])
        self.client = GeminiClient(
            model_name=os.getenv("MODEL_NAME", "gemini-1.5-flash"),
            api_key=os.getenv("GEMINI_API_KEY")
        )

    def _load_yaml(self, filename: str) -> dict:
        path = os.path.join(self.knowledge_dir, filename)
        if not os.path.exists(path):
            return {}
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    def scan_patch(self, patch_set: PatchSet) -> List[RuleViolation]:
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            pass
        return asyncio.run(self._async_scan(patch_set))
        
    async def _async_scan(self, patch_set: PatchSet) -> List[RuleViolation]:
        violations = []
        if not self.regressions:
            return violations
            
        regressions_text = "\n".join([f"{r.get('id')}: {r.get('title')}" for r in self.regressions])
        
        for op in patch_set.operations:
            if not op.new_content:
                continue
                
            prompt = f"""You are the Knowledge Memory Verifier.
Check if the following code introduces any of these known past regressions:
{regressions_text}

If it introduces a regression, output REJECT: followed by the regression ID and reason.
If it is safe, output OK.

Patch:
{op.new_content}
"""
            result = await self.client.create(
                messages=[SystemMessage(content=prompt)]
            )
            
            content_str = str(result.content)
            if "REJECT:" in content_str:
                reason = content_str.split("REJECT:", 1)[-1].strip()
                violations.append(
                    RuleViolation(
                        severity="CRITICAL",
                        category="Regression",
                        file=op.path,
                        line=1,
                        message=f"Regression detected: {reason}",
                        suggestion="Review knowledge base to understand past decisions."
                    )
                )
        return violations
