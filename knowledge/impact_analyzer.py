import os
import json
from typing import List
from orchestrator.gemini_client import GeminiClient
from schemas.impact_report import ImpactReport
from autogen_core.models import SystemMessage

class ImpactAnalyzer:
    def __init__(self):
        self.client = GeminiClient(
            model_name=os.getenv("MODEL_NAME", "gemini-1.5-flash"),
            api_key=os.getenv("GEMINI_API_KEY")
        )

    async def predict_impact(self, feature_request: str, dependency_graph_path: str) -> ImpactReport:
        graph_data = ""
        if os.path.exists(dependency_graph_path):
            with open(dependency_graph_path, 'r', encoding='utf-8') as f:
                graph_data = f.read()

        prompt = f"""You are the Impact Analyzer. 
Given the following feature request and the dependency graph of the repository, predict which files will need to be created or modified.
Output a JSON object EXACTLY in this schema:
{{
    "affected_files": ["app/api/mock_api.py", "app/models/BookingEntity.py", "lib/screens/loyalty.dart"],
    "reasoning": "Explain why these files."
}}

Feature Request:
{feature_request}

Dependency Graph:
{graph_data}
"""
        result = await self.client.create(
            messages=[SystemMessage(content=prompt)]
        )
        
        content = result.content
        affected_files = []
        reasoning = ""
        
        try:
            start = content.find("{")
            end = content.rfind("}") + 1
            if start != -1 and end != -1:
                data = json.loads(content[start:end])
                affected_files = data.get("affected_files", [])
                reasoning = data.get("reasoning", "")
        except Exception:
            pass
            
        return ImpactReport(feature_request=feature_request, affected_files=affected_files, reasoning=reasoning)
