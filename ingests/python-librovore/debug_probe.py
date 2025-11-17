#!/usr/bin/env python3
"""
Debug script to test probe_url functionality on pytest.org objects.inv
"""

import asyncio
import sys
from pathlib import Path
from urllib.parse import urlparse

# Add the source directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "sources"))

import librovore.cacheproxy as cacheproxy
import librovore.state as state

async def test_probe():
    """Test probe_url functionality directly."""

    print("=== Testing probe_url on pytest.org objects.inv ===\n")

    # Create caches
    robots_cache = cacheproxy.RobotsCache()
    probe_cache = cacheproxy.ProbeCache(robots_cache=robots_cache)

    # URL to test
    url_str = "https://docs.pytest.org/en/latest/objects.inv"
    url = urlparse(url_str)

    print(f"Testing URL: {url_str}")

    try:
        result = await cacheproxy.probe_url(probe_cache, url)
        print(f"✅ Probe result: {result}")
        print(f"   Type: {type(result)}")
    except Exception as exc:
        print(f"❌ Probe failed: {type(exc).__name__}: {exc}")
        import traceback
        print("\nFull traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_probe())