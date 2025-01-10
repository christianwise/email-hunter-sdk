"""Rate limiting implementation."""

import time
from collections import deque
from threading import Lock
from typing import Deque


class RateLimiter:
    """Thread-safe rate limiter implementation."""

    def __init__(self, max_requests: int, time_window: float = 60.0) -> None:
        """Initialize rate limiter.

        Args:
            max_requests: Maximum number of requests allowed in time window
            time_window: Time window in seconds
        """
        self._max_requests = max_requests
        self._time_window = time_window
        self._requests: Deque[float] = deque()
        self._lock = Lock()

    def acquire(self) -> None:
        """Acquire permission to make a request.

        This method blocks until a request can be made without
        exceeding the rate limit.
        """
        with self._lock:
            now = time.time()
            
            # Remove expired timestamps
            while self._requests and now - self._requests[0] > self._time_window:
                self._requests.popleft()
            
            # If we've hit the limit, wait until we can make another request
            if len(self._requests) >= self._max_requests:
                sleep_time = self._requests[0] + self._time_window - now
                if sleep_time > 0:
                    time.sleep(sleep_time)
                    self._requests.popleft()
            
            self._requests.append(now) 