#!/usr/bin/env python3

# Test with cache-busting headers
import asyncio
import sys
import os

# Add the source directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'sources'))

from librovore.structures.mkdocs.extraction import extract_contents
import httpx

async def test_cache_bypass():
    # Test with explicit cache bypass
    objects = [{
        'name': 'pydantic.BaseModel',
        'role': 'class', 
        'domain': 'py',
        'priority': '1',
        'uri': 'api/base_model/#pydantic.BaseModel'
    }]
    
    print("=== Testing extract_contents directly ===")
    results = await extract_contents(
        'https://docs.pydantic.dev/latest/',
        objects,
        theme='material',
        include_snippets=True
    )
    
    if results:
        result = results[0]
        print(f"Description: {repr(result['description'])}")
        print(f"Content snippet: {repr(result['content_snippet'])}")
    else:
        print("No results returned")

if __name__ == "__main__":
    asyncio.run(test_cache_bypass())