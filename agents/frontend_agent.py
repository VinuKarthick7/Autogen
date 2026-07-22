import os
from autogen_agentchat.agents import AssistantAgent
from orchestrator.gemini_client import GeminiClient

class FrontendAgent(AssistantAgent):
    def __init__(self, conventions, plan):
        client = GeminiClient(
            model_name=os.getenv("MODEL_NAME", "gemini-1.5-flash"),
            api_key=os.getenv("GEMINI_API_KEY")
        )
        sys_msg = f"""You are the Frontend Agent.
Your job is to generate flutter code based on this plan:
{plan.model_dump_json()}

Conventions:
{conventions.model_dump_json()}

Output your response as JSON:
{{
  "files": [
    {{
      "path": "lib/screens/filename.dart",
      "content": "file contents here",
      "file_type": "dart"
    }}
  ]
}}
"""
        super().__init__(
            name="frontend",
            model_client=client,
            system_message=sys_msg,
            description="Generates Flutter frontend code."
        )
