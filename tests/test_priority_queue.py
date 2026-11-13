import asyncio
import unittest
from runner.priority_queue import PriorityTaskQueue

class TestPriorityTaskQueue(unittest.IsolatedAsyncioTestCase):
    async def test_priority_ordering(self):
        queue = PriorityTaskQueue(max_concurrency=2)
        exec_order = []

        async def make_task(val):
            exec_order.append(val)
            return val

        # Submit in non-priority order
        await queue.submit(priority=10, task_id="t10", coro_fn=lambda: make_task("low"))
        await queue.submit(priority=1, task_id="t1", coro_fn=lambda: make_task("urgent"))
        await queue.submit(priority=5, task_id="t5", coro_fn=lambda: make_task("medium"))

        res1 = await queue.run_next()
        res2 = await queue.run_next()
        res3 = await queue.run_next()

        self.assertEqual(res1[0], "t1")
        self.assertEqual(res2[0], "t5")
        self.assertEqual(res3[0], "t10")
        self.assertEqual(exec_order, ["urgent", "medium", "low"])
        self.assertEqual(queue.completed_count, 3)

    async def test_cancellation(self):
        queue = PriorityTaskQueue(max_concurrency=2)
        await queue.submit(priority=1, task_id="cancellable", coro_fn=lambda: asyncio.sleep(0.01))
        await queue.submit(priority=2, task_id="remaining", coro_fn=lambda: asyncio.sleep(0.01))

        queue.cancel("cancellable")
        res = await queue.run_next()
        self.assertEqual(res[0], "remaining")

if __name__ == "__main__":
    unittest.main()
