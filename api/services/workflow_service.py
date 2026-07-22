from api.services.run_service import RunService
from api.workers.queue import JobQueue

class WorkflowService:
    def __init__(self):
        self.run_service = RunService()
        self.queue = JobQueue()

    async def start_workflow(self, request):
        status = self.run_service.create_run(request)
        # Enqueue job
        await self.queue.enqueue("execute_workflow", run_id=status.run_id)
        return status
        
    async def get_status(self, run_id: str):
        return self.run_service.get_status(run_id)
        
    async def list_runs(self):
        return self.run_service.list_runs()
        
    async def cancel_workflow(self, run_id: str):
        await self.queue.cancel(run_id)
        # Update status
        try:
            status = self.run_service.get_status(run_id)
            if status.status in ["queued", "running", "verifying", "repairing"]:
                status.status = "failed"
                self.run_service.update_status(run_id, status)
        except FileNotFoundError:
            pass
            
    async def cleanup_run(self, run_id: str):
        import shutil
        import os
        run_dir = self.run_service._get_run_dir(run_id)
        if os.path.exists(run_dir):
            shutil.rmtree(run_dir)
