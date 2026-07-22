import os
from autogen_agentchat.agents import AssistantAgent
from orchestrator.gemini_client import GeminiClient

class DatabaseAgent(AssistantAgent):
    def __init__(self, conventions, plan):
        client = GeminiClient(
            model_name=os.getenv("MODEL_NAME", "gemini-1.5-flash"),
            api_key=os.getenv("GEMINI_API_KEY")
        )
        sys_msg = f"""You are the Database Agent.
Your job is to generate database models based on this plan:
{plan.model_dump_json()}

Conventions:
{conventions.model_dump_json()}

Output your response as JSON:
{{
  "files": [
    {{
      "path": "app/models/filename.py",
      "content": "file contents here",
      "file_type": "python"
    }}
  ]
}}
"""
        super().__init__(
            name="database",
            model_client=client,
            system_message=sys_msg,
            description="Generates database models and migrations."
        )
