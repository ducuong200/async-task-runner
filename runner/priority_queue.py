import asyncio
import heapq
import time
from typing import Any, Callable, Coroutine, Dict, List, Optional, Tuple

class PriorityTask:
    def __init__(self, priority: int, task_id: str, coro_fn: Callable[[], Coroutine[Any, Any, Any]]):
        self.priority = priority
        self.task_id = task_id
        self.coro_fn = coro_fn
        self.created_at = time.time()

    def __lt__(self, other: "PriorityTask") -> bool:
        if self.priority != other.priority:
            return self.priority < other.priority
        return self.created_at < other.created_at

class PriorityTaskQueue:
    """Asynchronous priority task queue with bounded worker concurrency."""
    def __init__(self, max_concurrency: int = 4):
        self.max_concurrency = max_concurrency
        self._heap: List[PriorityTask] = []
        self._lock = asyncio.Lock()
        self._semaphore = asyncio.Semaphore(max_concurrency)
        self._cancelled_tasks = set()
        self._completed_count = 0

    async def submit(self, priority: int, task_id: str, coro_fn: Callable[[], Coroutine[Any, Any, Any]]) -> None:
        async with self._lock:
            heapq.heappush(self._heap, PriorityTask(priority, task_id, coro_fn))

    def cancel(self, task_id: str) -> None:
        self._cancelled_tasks.add(task_id)

    async def run_next(self) -> Optional[Tuple[str, Any]]:
        async with self._lock:
            while self._heap:
                task = heapq.heappop(self._heap)
                if task.task_id in self._cancelled_tasks:
                    continue
                break
            else:
                return None

        async with self._semaphore:
            res = await task.coro_fn()
            self._completed_count += 1
            return task.task_id, res

    @property
    def pending_count(self) -> int:
        return len(self._heap)

    @property
    def completed_count(self) -> int:
        return self._completed_count
