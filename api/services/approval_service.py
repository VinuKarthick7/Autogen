from api.services.run_service import RunService
from api.workers.queue import JobQueue

class ApprovalService:
    def __init__(self):
        self.run_service = RunService()
        self.queue = JobQueue()
        
    async def approve(self, run_id: str, notes: str):
        status = self.run_service.get_status(run_id)
        if status.status != "waiting_approval":
            raise ValueError("Run is not waiting for approval")
            
        status.status = "completed"
        self.run_service.update_status(run_id, status)
        
        # In a real app we'd dispatch a job to finalize/commit the PR
        await self.queue.enqueue("finalize_commit", run_id=run_id, notes=notes)
        return status
        
    async def reject(self, run_id: str, notes: str):
        status = self.run_service.get_status(run_id)
        if status.status != "waiting_approval":
            raise ValueError("Run is not waiting for approval")
            
        status.status = "repairing"
        self.run_service.update_status(run_id, status)
        
        # Enqueue repair job
        await self.queue.enqueue("execute_repair", run_id=run_id, notes=notes)
        return status
        
    async def rollback(self, run_id: str):
        # Rollback via Git Sandbox
        pass
