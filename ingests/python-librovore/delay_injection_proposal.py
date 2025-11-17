#!/usr/bin/env python3
"""
Proposal: Dependency Injection for Delay Function

Instead of patching asyncio.sleep globally, inject a delay function that can be:
1. Real asyncio.sleep in production
2. Mock/no-op in tests
3. Configurable for different environments
"""

from typing import Callable, Awaitable
import asyncio

# Define the delay function type
DelayFunction = Callable[[float], Awaitable[None]]

# Default production delay function
async def real_delay(seconds: float) -> None:
    """Production delay using asyncio.sleep."""
    await asyncio.sleep(seconds)

# Test delay function (no-op)
async def no_delay(seconds: float) -> None:
    """Test delay that doesn't actually sleep."""
    pass

# Mock delay function for testing specific behavior
class MockDelay:
    def __init__(self):
        self.calls = []
    
    async def __call__(self, seconds: float) -> None:
        self.calls.append(seconds)
        # Don't actually sleep

# Current problematic approach in cacheproxy.py:
async def _apply_request_delay_old(url, robots_cache=None):
    # ...
    if delay_remaining > 0:
        await asyncio.sleep(delay_remaining)  # Hard-coded!

# Better approach with dependency injection:
async def _apply_request_delay_new(
    url, 
    robots_cache=None,
    delay_fn: DelayFunction = real_delay  # Injected dependency
):
    # ...
    if delay_remaining > 0:
        await delay_fn(delay_remaining)  # Configurable!

# Configuration class could include delay function
class CacheConfiguration:
    def __init__(self, delay_fn: DelayFunction = real_delay):
        self.delay_fn = delay_fn
        # ... other config

# Usage in tests:
def test_with_no_delay():
    config = CacheConfiguration(delay_fn=no_delay)
    # Test runs fast without real sleeps

def test_with_mock_delay():
    mock_delay = MockDelay()
    config = CacheConfiguration(delay_fn=mock_delay)
    # Can verify delay was called with correct duration
    assert mock_delay.calls == [2.0]