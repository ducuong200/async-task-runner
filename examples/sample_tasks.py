import asyncio
from runner.engine import TaskRunner
from runner.retry import with_retry

async def dummy_job(job_id: int):
    await asyncio.sleep(0.1)
    return f"Job {job_id} complete"

async def main():
    runner = TaskRunner(concurrency=3)
    tasks = [runner.execute(f"task-{i}", lambda i=i: dummy_job(i)) for i in range(5)]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    print("Execution results:", results)

if __name__ == "__main__":
    asyncio.run(main())
