import random
from typing import Optional

class ExponentialBackoffWithJitter:
    """Calculates exponential backoff delay with full jitter for distributed systems."""
    def __init__(self, base_delay: float = 0.5, max_delay: float = 30.0, factor: float = 2.0):
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.factor = factor

    def calculate_delay(self, attempt: int) -> float:
        calculated = min(self.max_delay, self.base_delay * (self.factor ** max(0, attempt)))
        return random.uniform(0.0, calculated)
