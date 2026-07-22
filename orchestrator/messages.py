import json
import os
from datetime import datetime
from autogen_agentchat.messages import TextMessage
from schemas.agent_message import AgentMessage

def to_agent_message(autogen_msg) -> AgentMessage:
    sender = getattr(autogen_msg, "source", "unknown")
    content = ""
    
    # In newer autogen-agentchat, content can be a string or a list of items
    if hasattr(autogen_msg, "content"):
        if isinstance(autogen_msg.content, str):
            content = autogen_msg.content
        else:
            # Simple serialization if it's a list (e.g. text blocks)
            content = str(autogen_msg.content)
            
    return AgentMessage(
        sender=sender,
        message=content,
        timestamp=datetime.utcnow()
    )

def export_chat(messages: list[AgentMessage], path: str = "logs/team_chat.json"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump([m.model_dump(mode="json") for m in messages], f, indent=2)
