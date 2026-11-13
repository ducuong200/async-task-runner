import unittest
from runner.backoff import ExponentialBackoffWithJitter

class TestExponentialBackoff(unittest.TestCase):
    def test_calculate_delay_bounds(self):
        backoff = ExponentialBackoffWithJitter(base_delay=1.0, max_delay=10.0, factor=2.0)
        for attempt in range(5):
            delay = backoff.calculate_delay(attempt)
            self.assertGreaterEqual(delay, 0.0)
            self.assertLessEqual(delay, 10.0)

    def test_max_delay_cap(self):
        backoff = ExponentialBackoffWithJitter(base_delay=1.0, max_delay=5.0, factor=2.0)
        delay = backoff.calculate_delay(10)
        self.assertLessEqual(delay, 5.0)

if __name__ == "__main__":
    unittest.main()
