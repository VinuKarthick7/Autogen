import os
import yaml
from typing import List
from schemas.patch_set import PatchSet
from schemas.rule_violation import RuleViolation
from orchestrator.gemini_client import GeminiClient
import asyncio
from autogen_core.models import UserMessage, SystemMessage

class DomainRulesEngine:
    def __init__(self):
        self.client = GeminiClient(
            model_name=os.getenv("MODEL_NAME", "gemini-1.5-flash"),
            api_key=os.getenv("GEMINI_API_KEY")
        )

    def scan_patch(self, patch_set: PatchSet) -> List[RuleViolation]:
        # Using the event loop to run async LLM call
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # We can't block easily if loop is running, but let's assume it runs via standard sync context or nest_asyncio
                # In this demo setup, we might be in a thread, so we can use asyncio.run
                pass
        except RuntimeError:
            pass
            
        return asyncio.run(self._async_scan(patch_set))
        
    async def _async_scan(self, patch_set: PatchSet) -> List[RuleViolation]:
        violations = []
        for op in patch_set.operations:
            if not op.new_content:
                continue
                
            prompt = f"""You are the Domain Logic Verifier.
Evaluate this patch against PMS invariants (e.g., overlapping bookings, illegal status transitions).
If the patch contains impossible logic (e.g. going from RESERVED to CLEANING without OCCUPIED),
output REJECT: followed by the reason.
If it is structurally sound, output OK.

Patch:
{op.new_content}
"""
            result = await self.client.create(
                messages=[SystemMessage(content=prompt)]
            )
            
            if "REJECT:" in str(result.content):
                reason = str(result.content).split("REJECT:", 1)[-1].strip()
                violations.append(
                    RuleViolation(
                        severity="HIGH",
                        category="DomainLogic",
                        file=op.path,
                        line=1,
                        message=f"Domain invariant violation: {reason}",
                        suggestion="Fix domain logic transitions."
                    )
                )
        return violations
