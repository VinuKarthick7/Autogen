import os
from typing import Sequence, Any, Dict, List, Mapping, Optional
from autogen_core.models import (
    ChatCompletionClient, CreateResult, ModelInfo,
    SystemMessage, UserMessage, AssistantMessage, LLMMessage, RequestUsage
)
from google import genai
from google.genai import types

class ModelCapabilities:
    vision: bool = False
    function_calling: bool = True
    json_output: bool = True

class GeminiClient(ChatCompletionClient):
    def __init__(self, model_name: str = None, api_key: str = None):
        self.model_name = model_name or os.getenv("MODEL_NAME", "gemini-1.5-flash")
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=self.api_key)
        
    async def create(self, messages: Sequence[LLMMessage], **kwargs) -> CreateResult:
        sys_msg = ""
        contents = []
        for m in messages:
            if isinstance(m, SystemMessage):
                sys_msg += m.content + "\n"
            elif isinstance(m, UserMessage):
                contents.append(types.Content(role="user", parts=[types.Part.from_text(text=str(m.content))]))
            elif isinstance(m, AssistantMessage):
                contents.append(types.Content(role="model", parts=[types.Part.from_text(text=str(m.content))]))
                
        config = types.GenerateContentConfig()
        if sys_msg:
            config.system_instruction = sys_msg
            
        import asyncio
        import random
        import json
        import os
        from datetime import datetime
        
        # MOCK RESPONSE TO AVOID 20 RPD RATE LIMITS
        await asyncio.sleep(0.5)
        mock_response = ""
        
        # Determine the agent context by examining system messages
        if "Reviewer" in sys_msg:
            if '"passed": false' in sys_msg:
                mock_response = "REJECT\nLint failed"
            else:
                mock_response = "APPROVE"
        elif "Planner" in sys_msg:
            mock_response = json.dumps({"feature_name": "Mock", "description": "Mock plan", "database_changes": [], "backend_changes": [], "frontend_changes": []})
        elif "Database" in sys_msg:
            mock_response = json.dumps({"files": [{"path": "app/models/BookingEntity.py", "content": "class BookingEntity:\n    uuid = '123'\n    guestId = '456'\n    # Missing propertyId\n    def change_status(self):\n        print('RESERVED to CLEANING')\n", "file_type": "python"}]})
        elif "Backend" in sys_msg:
            mock_response = json.dumps({"files": [{"path": "app/api/backend_api.py", "content": "def backend_router() -> int:\n    return 1\n", "file_type": "python"}]})
        elif "Frontend" in sys_msg:
            mock_response = json.dumps({"files": [{"path": "lib/screens/frontend.dart", "content": "class FrontendScreen", "file_type": "dart"}]})
        elif "Domain Logic Verifier" in sys_msg:
            if "print('RESERVED to CLEANING')" in sys_msg or "store.box<" in sys_msg:
                mock_response = "REJECT: Impossible status transition."
            else:
                mock_response = "OK"
        elif "Guided Repair Agent" in sys_msg:
            # We simulate a successful repair patch
            mock_response = json.dumps({"operations": [{"operation": "modify", "path": "app/models/BookingEntity.py", "new_content": "class BookingEntity:\n    uuid = '123'\n    guestId = '456'\n    roomId = '789'\n    propertyId = '000'\n", "reason": "Fixed missing fields"}]})
        elif "Knowledge Memory Verifier" in sys_msg:
            if "password == '1234'" in sys_msg:
                mock_response = "REJECT: PMS-001 Authentication bypass using 1234"
            else:
                mock_response = "OK"
        else:
            mock_response = "Next speaker please"

        return CreateResult(
            content=mock_response,
            usage=RequestUsage(prompt_tokens=10, completion_tokens=10),
            finish_reason="stop",
            cached=False
        )

    def count_tokens(self, messages: Sequence[LLMMessage], **kwargs) -> int:
        return 0

    @property
    def model_info(self) -> ModelInfo:
        return ModelInfo(vision=False, function_calling=True, json_output=True, family="gemini")

    def remaining_tokens(self) -> int:
        return 1000000

    @property
    def capabilities(self):
        return ModelCapabilities()
        
    def actual_usage(self) -> RequestUsage:
        return RequestUsage(prompt_tokens=0, completion_tokens=0)
        
    def total_usage(self) -> RequestUsage:
        return RequestUsage(prompt_tokens=0, completion_tokens=0)
        
    async def create_stream(self, messages: Sequence[LLMMessage], **kwargs) -> Any:
        yield await self.create(messages, **kwargs)
        
    def close(self) -> None:
        pass
