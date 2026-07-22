import json
import asyncio
from typing import Dict, List
from fastapi import WebSocket
from api.schemas.websocket_event import WebsocketEvent

class WebsocketService:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
        
    async def connect(self, run_id: str, websocket: WebSocket):
        await websocket.accept()
        if run_id not in self.active_connections:
            self.active_connections[run_id] = []
        self.active_connections[run_id].append(websocket)
        
    def disconnect(self, run_id: str, websocket: WebSocket):
        if run_id in self.active_connections:
            self.active_connections[run_id].remove(websocket)
            if not self.active_connections[run_id]:
                del self.active_connections[run_id]
                
    async def broadcast(self, event: WebsocketEvent):
        run_id = event.run_id
        if run_id in self.active_connections:
            for connection in self.active_connections[run_id]:
                try:
                    await connection.send_text(event.model_dump_json())
                except Exception:
                    pass
                    
    async def publish_event(self, event: WebsocketEvent):
        import os
        # Also persist to file for replay
        event_dir = os.path.join("storage", "websocket", event.run_id)
        os.makedirs(event_dir, exist_ok=True)
        with open(os.path.join(event_dir, "events.jsonl"), "a") as f:
            f.write(event.model_dump_json() + "\n")
        await self.broadcast(event)
        
    async def subscribe(self, run_id: str):
        pass # Not used directly when we have broadcast
