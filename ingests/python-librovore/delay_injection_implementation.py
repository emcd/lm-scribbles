#!/usr/bin/env python3
"""
Concrete implementation proposal for delay function dependency injection.

This approach is much cleaner than global asyncio.sleep patching.
"""

import asyncio
from typing import Callable, Awaitable

# 1. Define the delay function type
DelayFunction = Callable[[float], Awaitable[None]]

# 2. Default implementations
async def production_delay(seconds: float) -> None:
    """Production delay using real asyncio.sleep."""
    await asyncio.sleep(seconds)

async def test_delay(seconds: float) -> None:
    """Test delay that doesn't actually sleep."""
    pass  # No-op for fast tests

# 3. Update CacheConfiguration to include delay function
class CacheConfiguration:
    def __init__(
        self,
        # ... existing parameters ...
        delay_fn: DelayFunction = production_delay
    ):
        # ... existing initialization ...
        self.delay_fn = delay_fn

# 4. Update _apply_request_delay to accept injected delay function
async def _apply_request_delay(
    url,
    robots_cache=None,
    client_factory=None,
    delay_fn: DelayFunction = None  # Optional override
):
    # Use injected delay function or get from cache config
    if delay_fn is None:
        delay_fn = robots_cache._configuration.delay_fn if robots_cache else production_delay
    
    # ... existing logic for calculating delay ...
    delay_remaining = robots_cache.calculate_delay_remainder(domain)
    
    if delay_remaining > 0:
        await delay_fn(delay_remaining)  # Use injected function!

# 5. Test fixtures can provide no-op delay
@pytest.fixture
def fast_cache_config():
    """Cache configuration with no delays for fast tests."""
    return CacheConfiguration(delay_fn=test_delay)

# 6. Tests can use fast configuration
async def test_some_function(fast_cache_config):
    result = await retrieve_url(
        "https://example.com/test", 
        cache=ContentCache(fast_cache_config)
    )
    # Runs fast without real sleeps!

# 7. Or tests can mock delay function directly
async def test_delay_behavior():
    mock_delay = Mock()
    await _apply_request_delay(
        url, 
        robots_cache=cache, 
        delay_fn=mock_delay
    )
    mock_delay.assert_called_once_with(2.0)  # Verify delay was requested