import asyncio
from api.workers.queue import JobQueue
from api.services.benchmark_service import BenchmarkService

class BenchmarkExecutor:
    def __init__(self):
        self.queue = JobQueue()
        self.benchmark_service = BenchmarkService()
        
    async def process_job(self, payload):
        job_name = payload.get("job")
        args = payload.get("args", {})
        
        if job_name == "execute_benchmark":
            # Just printing out for now.
            print(f"Executing benchmark suite: {args.get('suite')}")
            # In a real environment, we'd spawn the actual benchmark.py subprocess
            # e.g., subprocess.run(["python", "benchmark.py", "--suite", args.get('suite')])

    async def run(self):
        print("Benchmark Worker listening...")
        while True:
            try:
                payload = await self.queue.dequeue()
                if payload:
                    print(f"Received benchmark job: {payload}")
                    await self.process_job(payload)
            except Exception as e:
                print(f"Worker Error: {e}")
            await asyncio.sleep(0.1)

if __name__ == "__main__":
    executor = BenchmarkExecutor()
    asyncio.run(executor.run())
