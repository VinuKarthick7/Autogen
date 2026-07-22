import os
import json
from typing import Dict, Any, List
from datetime import datetime

class ReplayEngine:
    def __init__(self, artifacts_dir: str = "artifacts"):
        self.artifacts_dir = artifacts_dir

    def list_runs(self) -> List[Dict[str, Any]]:
        runs = []
        if not os.path.exists(self.artifacts_dir):
            return runs
            
        for run_id in os.listdir(self.artifacts_dir):
            run_path = os.path.join(self.artifacts_dir, run_id)
            if os.path.isdir(run_path):
                chat_path = os.path.join(run_path, "chat.json")
                if os.path.exists(chat_path):
                    timestamp = os.path.getmtime(chat_path)
                    runs.append({
                        "run_id": run_id,
                        "timestamp": timestamp,
                        "date": datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
                    })
        return sorted(runs, key=lambda x: x["timestamp"], reverse=True)

    def load_run(self, run_id: str) -> Dict[str, Any]:
        run_path = os.path.join(self.artifacts_dir, run_id)
        if not os.path.exists(run_path):
            raise FileNotFoundError(f"Run {run_id} not found in {self.artifacts_dir}")
            
        data = {}
        for file in ["plan.json", "chat.json", "generated_files.json", "validation.json"]:
            filepath = os.path.join(run_path, file)
            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    try:
                        data[file.split(".")[0]] = json.load(f)
                    except json.JSONDecodeError:
                        data[file.split(".")[0]] = None
        return data

    def print_transcript(self, run_id: str):
        data = self.load_run(run_id)
        chat = data.get("chat", [])
        if not chat:
            print(f"No chat transcript found for Run {run_id}")
            return
            
        print(f"--- Transcript for Run {run_id} ---\n")
        
        for msg in chat:
            sender = msg.get("sender", "unknown")
            content = msg.get("message", "")
            
            if len(content) > 500:
                content = content[:500] + "... [truncated]"
                
            print(f"[{sender.upper()}] ->\n{content}\n")

    def export_files(self, run_id: str, target_dir: str):
        data = self.load_run(run_id)
        files = data.get("generated_files", [])
        
        if not files:
            print(f"No generated files found for Run {run_id}")
            return
            
        os.makedirs(target_dir, exist_ok=True)
        for f in files:
            file_path = os.path.join(target_dir, f.get("path", ""))
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as out:
                out.write(f.get("content", ""))
        
        print(f"Exported {len(files)} files to {target_dir}")
