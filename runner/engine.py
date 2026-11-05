import asyncio
import time
from typing import Callable, Any, List, Dict

class TaskRunner:
    def __init__(self, concurrency: int = 5):
        self.concurrency = concurrency
        self.semaphore = asyncio.Semaphore(concurrency)
        self.results: Dict[str, Any] = {}

    async def execute(self, task_id: str, coro_fn: Callable[[], Any]) -> Any:
        async with self.semaphore:
            start = time.time()
            try:
                res = await coro_fn()
                elapsed = time.time() - start
                self.results[task_id] = {"status": "success", "result": res, "elapsed": elapsed}
                return res
            except Exception as e:
                elapsed = time.time() - start
                self.results[task_id] = {"status": "failed", "error": str(e), "elapsed": elapsed}
                raise
