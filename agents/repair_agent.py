import os
import json
from autogen_agentchat.agents import AssistantAgent
from orchestrator.gemini_client import GeminiClient

class RepairAgent(AssistantAgent):
    def __init__(self, name="Repair_Agent"):
        client = GeminiClient(
            model_name=os.getenv("MODEL_NAME", "gemini-1.5-flash"),
            api_key=os.getenv("GEMINI_API_KEY")
        )
        sys_msg = """You are the Guided Repair Agent.
You will receive a patch containing original feature generation and specific verification failures.
Your job is to generate a fix EXACTLY for these failures.
Do not modify unrelated files. Do not introduce new APIs. Do not bypass repository rules.
Output your response as JSON in the PatchSet schema format (PatchSet -> list of PatchOperation).
Example:
{
    "operations": [
        {
            "operation": "modify",
            "path": "app/models/BookingEntity.py",
            "new_content": "class BookingEntity:\n...",
            "reason": "Fixing missing roomId field"
        }
    ]
}"""
        super().__init__(
            name=name,
            model_client=client,
            system_message=sys_msg,
        )
