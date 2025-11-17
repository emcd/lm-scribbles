#!/usr/bin/env python3

import asyncio
import json
import sys
sys.path.insert(0, 'sources')

async def test_mcp_functions():
    from sphinxmcps import functions
    from sphinxmcps.__main__ import _prepare
    from sphinxmcps.xtnsmgr import initialize_container
    import contextlib
    
    async with contextlib.AsyncExitStack() as exits:
        auxdata = await _prepare(environment=True, exits=exits, logfile=None)
        await initialize_container(auxdata)
        
        source = '.auxiliary/artifacts/sphinx-html'
        
        print("=== Testing query_inventory ===")
        result = await functions.query_inventory(source, 'sphinx', results_max=2)
        print("Has documents with fuzzy_score:")
        for doc in result.get('documents', []):
            if 'fuzzy_score' in doc:
                print(f"  {doc['name']}: fuzzy_score = {doc['fuzzy_score']}")
        print()
        
        print("=== Testing query_content ===")
        result = await functions.query_content(source, 'sphinx', results_max=2)
        print("Has documents with fuzzy_score:")
        for doc in result.get('documents', []):
            if 'fuzzy_score' in doc:
                print(f"  {doc['name']}: fuzzy_score = {doc['fuzzy_score']}")
        print()
        
        print("=== Testing summarize_inventory ===")
        result_str = await functions.summarize_inventory(source)
        print("Summary contains 'fuzzy_score':", 'fuzzy_score' in result_str)
        print()

if __name__ == '__main__':
    asyncio.run(test_mcp_functions())