import json
import redis.asyncio as redis
import os

class JobQueue:
    def __init__(self):
        redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379")
        self.redis = redis.from_url(redis_url)
        self.queue_name = "autogen_jobs"
        
    async def enqueue(self, job_name: str, **kwargs):
        payload = json.dumps({"job": job_name, "args": kwargs})
        await self.redis.rpush(self.queue_name, payload)
        
    async def dequeue(self):
        result = await self.redis.blpop(self.queue_name, timeout=1)
        if result:
            _, payload = result
            return json.loads(payload)
        return None
        
    async def cancel(self, run_id: str):
        # Redis list doesn't have easy removal by property, we can just mark it cancelled in a hash
        await self.redis.hset("cancelled_jobs", run_id, "1")
        
    async def get_position(self, run_id: str) -> int:
        return 0 # Simplified
