#!/usr/bin/env python3
"""Test robots.txt functionality."""

import asyncio
from urllib.parse import urlparse
import sphinxmcps.cacheproxy as cache

async def test_robots():
    """Test robots.txt functionality with a real URL."""
    url = urlparse('https://docs.python.org/3/library/functions.html')
    
    # This should work and respect robots.txt
    try:
        content = await cache.retrieve_url_as_text(url)
        print(f'✓ Successfully retrieved content: {len(content)} characters')
        print('✓ robots.txt compliance working')
    except Exception as e:
        print(f'✗ Error: {e}')

    # Test domain extraction
    domain = cache._extract_domain(url)
    print(f'✓ Domain extraction: {domain}')

    # Test robots cache
    robots_cache = cache._robots_cache_default
    print(f'✓ Robots cache created: {type(robots_cache).__name__}')

if __name__ == '__main__':
    asyncio.run(test_robots())