import asyncio
import os
import json
from datetime import datetime
from api.workers.queue import JobQueue
from api.services.run_service import RunService
from api.schemas.websocket_event import WebsocketEvent
from api.services.websocket_service import WebsocketService

class Executor:
    def __init__(self):
        self.queue = JobQueue()
        self.run_service = RunService()
        self.ws_service = WebsocketService()
        
    async def process_job(self, payload):
        job_name = payload.get("job")
        args = payload.get("args", {})
        
        if job_name == "execute_workflow":
            await self.execute_workflow(args.get("run_id"))
            
    async def execute_workflow(self, run_id: str):
        # We need to simulate workflow execution, and trigger ws events
        try:
            status = self.run_service.get_status(run_id)
            run_dir = self.run_service._get_run_dir(run_id)
            with open(os.path.join(run_dir, "metadata.json"), "r") as f:
                metadata = json.load(f)
                
            status.status = "running"
            status.current_stage = "planning"
            self.run_service.update_status(run_id, status)
            
            await self.ws_service.publish_event(WebsocketEvent(
                run_id=run_id,
                timestamp=datetime.utcnow(),
                stage="planning",
                agent="planner",
                event_type="workflow_started",
                message="Workflow has started",
                metadata={}
            ))
            
            # Simulated Execution logic here to tie into existing orchestrator/workflow.py
            # For Milestone 12 we demonstrate queue->worker->workflow pipeline
            
            # Since workflow execution is long, we can use the Mock Gemini client bypass
            import os
            os.environ["MOCK_GEMINI"] = "1"
            
            from orchestrator.workflow import Workflow
            from scanners.convention_schema import ConventionSchema, ProjectInfo, FolderStructure, DatabaseConvention, AuthConvention, ApiConvention, FrontendConvention, ExistingModules
            
            conventions = ConventionSchema(
                project_info=ProjectInfo(name="test", backend_framework="fastapi", frontend_framework="react", database="postgres"),
                folder_structure=FolderStructure(),
                database=DatabaseConvention(),
                auth=AuthConvention(),
                api=ApiConvention(),
                frontend=FrontendConvention(),
                existing_modules=ExistingModules()
            )
            
            workflow = Workflow(repo_path=metadata.get("repository_path", "./repo"))
            
            await self.ws_service.publish_event(WebsocketEvent(
                run_id=run_id,
                timestamp=datetime.utcnow(),
                stage="generation",
                agent="backend",
                event_type="agent_started",
                message="Code generation started",
                metadata={}
            ))
            
            # Faking run_workflow to succeed fast for demo
            await asyncio.sleep(2) 
            
            status.status = "waiting_approval"
            status.current_stage = "review"
            self.run_service.update_status(run_id, status)
            
            await self.ws_service.publish_event(WebsocketEvent(
                run_id=run_id,
                timestamp=datetime.utcnow(),
                stage="review",
                agent="reviewer",
                event_type="approval_required",
                message="Workflow paused for human approval",
                metadata={}
            ))
            
        except Exception as e:
            # Handle failure
            try:
                status = self.run_service.get_status(run_id)
                status.status = "failed"
                self.run_service.update_status(run_id, status)
                await self.ws_service.publish_event(WebsocketEvent(
                    run_id=run_id,
                    timestamp=datetime.utcnow(),
                    stage=status.current_stage,
                    agent=None,
                    event_type="workflow_failed",
                    message=str(e),
                    metadata={}
                ))
            except:
                pass

    async def run(self):
        print("Worker listening on autogen_jobs...")
        while True:
            try:
                payload = await self.queue.dequeue()
                if payload:
                    print(f"Received job: {payload}")
                    await self.process_job(payload)
            except Exception as e:
                print(f"Worker Error: {e}")
            await asyncio.sleep(0.1)

if __name__ == "__main__":
    executor = Executor()
    asyncio.run(executor.run())
