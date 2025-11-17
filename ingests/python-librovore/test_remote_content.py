#!/usr/bin/env python3

import sys
import asyncio
sys.path.insert(0, 'sources')

async def test_remote_content():
    """Test content extraction against remote Sphinx sites"""
    from sphinxmcps import functions
    from sphinxmcps import xtnsmgr
    from sphinxmcps.cli import _prepare
    from sphinxmcps import interfaces
    import contextlib
    
    async with contextlib.AsyncExitStack() as exits:
        auxdata = await _prepare(environment=True, exits=exits, logfile=None)
        await xtnsmgr.register_processors(auxdata)
        
        test_sites = [
            ("https://docs.python.org/3/", "asyncio", "Python docs"),
            ("https://flask.palletsprojects.com/en/stable/", "flask", "Flask docs"),
            ("https://numpy.org/doc/stable/", "array", "NumPy docs")
        ]
        
        for source, query, site_name in test_sites:
            print(f"\n=== Testing {site_name} ===")
            print(f"Source: {source}")
            print(f"Query: {query}")
            
            try:
                result = await functions.query_content(
                    source,
                    query,
                    search_behaviors=interfaces.SearchBehaviors(
                        match_mode=interfaces.MatchMode.Fuzzy,
                        fuzzy_threshold=50
                    ),
                    filters={},
                    include_snippets=True,
                    results_max=3
                )
                
                print(f"Result keys: {result.keys()}")
                print(f"Results count: {len(result.get('documents', []))}")
                
                if result.get('documents'):
                    for i, doc in enumerate(result['documents'][:2]):
                        print(f"  Result {i+1}: {doc.get('object_name', 'N/A')}")
                        print(f"    Type: {doc.get('object_type', 'N/A')}")
                        print(f"    Domain: {doc.get('domain', 'N/A')}")
                        print(f"    Score: {doc.get('relevance_score', 'N/A')}")
                        snippet = doc.get('content_snippet', '')[:100]
                        print(f"    Snippet: {snippet}...")
                        
            except Exception as e:
                print(f"Error: {e}")
                import traceback
                traceback.print_exc()

if __name__ == '__main__':
    asyncio.run(test_remote_content())