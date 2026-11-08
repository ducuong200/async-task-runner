import asyncio
from typing import Callable, Any

async def with_retry(coro_fn: Callable[[], Any], max_retries: int = 3, delay: float = 1.0) -> Any:
    last_err = None
    for attempt in range(1, max_retries + 1):
        try:
            return await coro_fn()
        except Exception as e:
            last_err = e
            if attempt < max_retries:
                await asyncio.sleep(delay * attempt)
    raise last_err or RuntimeError("Task failed after retries")
