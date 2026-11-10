# async-task-runner

> Minimalist, robust asynchronous task orchestration and bounded worker pool for Python 3.10+.

## Highlights
- **Bounded Concurrency**: Controls active task bursts using asynchronous semaphores.
- **Backoff & Retries**: Automatic exponential retry strategies for transient network failures.
- **Execution Telemetry**: Lightweight in-memory tracking of elapsed runtimes and task statuses.
- **Zero Heavy Dependencies**: Pure standard library implementation with zero external baggage.

## Quick Start
```python
import asyncio
from runner.engine import TaskRunner

async def fetch_item(item_id: int):
    await asyncio.sleep(0.2)
    return {"id": item_id, "status": "ok"}

async def main():
    runner = TaskRunner(concurrency=4)
    tasks = [runner.execute(f"item-{i}", lambda i=i: fetch_item(i)) for i in range(10)]
    outcomes = await asyncio.gather(*tasks)
    print("Processed:", len(outcomes))

if __name__ == "__main__":
    asyncio.run(main())
```

## Running Verification
```bash
python3 examples/sample_tasks.py
```

## License
MIT
