#!/usr/bin/env python3
"""Test script to verify robots.txt fix works at functions layer."""

import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../sources'))

from librovore import functions, state, cacheproxy

async def test_pytest_docs():
    """Test pytest docs - previously failed with robots.txt 403"""
    print("Testing pytest docs inventory query...")

    # Create minimal global state like CLI would
    auxdata = state.Globals(configuration={})
    content_cache, probe_cache, robots_cache = cacheproxy.prepare(auxdata)
    auxdata.content_cache = content_cache
    auxdata.probe_cache = probe_cache
    auxdata.robots_cache = robots_cache

    try:
        result = await functions.query_inventory(
            auxdata=auxdata,
            location='https://docs.pytest.org/en/latest/',
            term='fixture'
        )
        print('SUCCESS: Got result:', type(result))
        if isinstance(result, dict) and 'results' in result:
            print('Results count:', len(result['results']))
        print('Result keys:', list(result.keys()) if isinstance(result, dict) else 'Not a dict')
        return True
    except Exception as e:
        print('ERROR:', type(e).__name__, ':', str(e))
        import traceback
        traceback.print_exc()
        return False

async def test_requests_docs():
    """Test requests docs - previously failed with robots.txt 403"""
    print("\nTesting requests docs inventory query...")

    auxdata = state.Globals(configuration={})
    content_cache, probe_cache, robots_cache = cacheproxy.prepare(auxdata)
    auxdata.content_cache = content_cache
    auxdata.probe_cache = probe_cache
    auxdata.robots_cache = robots_cache

    try:
        result = await functions.query_inventory(
            auxdata=auxdata,
            location='https://requests.readthedocs.io/en/latest/',
            term='requests.get'
        )
        print('SUCCESS: Got result:', type(result))
        if isinstance(result, dict) and 'results' in result:
            print('Results count:', len(result['results']))
        return True
    except Exception as e:
        print('ERROR:', type(e).__name__, ':', str(e))
        import traceback
        traceback.print_exc()
        return False

async def main():
    print("Testing robots.txt error handling fix...")

    success1 = await test_pytest_docs()
    success2 = await test_requests_docs()

    if success1 and success2:
        print("\n✅ Both tests passed - robots.txt fix working!")
    else:
        print("\n❌ Some tests failed - needs investigation")
        sys.exit(1)

if __name__ == '__main__':
    asyncio.run(main())