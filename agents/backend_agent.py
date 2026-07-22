import os
from autogen_agentchat.agents import AssistantAgent
from orchestrator.gemini_client import GeminiClient

class BackendAgent(AssistantAgent):
    def __init__(self, conventions, plan):
        client = GeminiClient(
            model_name=os.getenv("MODEL_NAME", "gemini-1.5-flash"),
            api_key=os.getenv("GEMINI_API_KEY")
        )
        sys_msg = f"""You are the Backend Agent.
Your job is to generate backend routers and services based on this plan:
{plan.model_dump_json()}

Conventions:
{conventions.model_dump_json()}

Output your response as JSON:
{{
  "files": [
    {{
      "path": "app/api/filename.py",
      "content": "file contents here",
      "file_type": "python"
    }}
  ]
}}
"""
        super().__init__(
            name="backend",
            model_client=client,
            system_message=sys_msg,
            description="Generates FastAPI routers, schemas, and services."
        )
