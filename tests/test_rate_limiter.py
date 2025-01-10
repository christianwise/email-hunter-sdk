"""Tests for rate limiter implementation."""

import time
from threading import Thread
from typing import List

import pytest

from hunter_sdk.utils.rate_limiter import RateLimiter


def test_rate_limiter_basic() -> None:
    """Test basic rate limiting functionality."""
    limiter = RateLimiter(max_requests=2, time_window=1.0)
    
    start_time = time.time()
    
    # First two requests should be immediate
    limiter.acquire()
    limiter.acquire()
    first_duration = time.time() - start_time
    assert first_duration < 0.1  # Should be near-instant
    
    # Third request should wait
    limiter.acquire()
    total_duration = time.time() - start_time
    assert total_duration >= 1.0  # Should wait for time window


def test_rate_limiter_threaded() -> None:
    """Test rate limiter in multi-threaded environment."""
    limiter = RateLimiter(max_requests=3, time_window=1.0)
    results: List[float] = []
    
    def worker() -> None:
        start = time.time()
        limiter.acquire()
        results.append(time.time() - start)
    
    threads = [Thread(target=worker) for _ in range(5)]
    start_time = time.time()
    
    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()
    
    # First 3 requests should be quick
    assert len([t for t in results if t < 0.1]) == 3
    # Last 2 should wait
    assert len([t for t in results if t >= 1.0]) == 2


def test_rate_limiter_window_reset() -> None:
    """Test that rate limit resets after time window."""
    limiter = RateLimiter(max_requests=1, time_window=0.5)
    
    # First request
    limiter.acquire()
    
    # Wait for window to reset
    time.sleep(0.6)
    
    # Second request should be immediate
    start_time = time.time()
    limiter.acquire()
    duration = time.time() - start_time
    assert duration < 0.1 