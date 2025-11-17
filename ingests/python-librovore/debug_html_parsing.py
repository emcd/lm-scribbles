#!/usr/bin/env python3

import sys
import asyncio  
sys.path.insert(0, 'sources')

async def debug_html_parsing():
    """Debug HTML parsing step for remote sites"""
    from sphinxmcps import functions
    from sphinxmcps import xtnsmgr
    from sphinxmcps.cli import _prepare
    from sphinxmcps import search
    from sphinxmcps import interfaces
    from sphinxmcps import __
    from sphinxmcps.processors.sphinx import extraction as _extraction
    from sphinxmcps.processors.sphinx import urls as _urls
    import contextlib
    
    async with contextlib.AsyncExitStack() as exits:
        auxdata = await _prepare(environment=True, exits=exits, logfile=None)
        await xtnsmgr.register_processors(auxdata)
        
        source = 'https://docs.python.org/3/'
        query = 'asyncio'
        
        # Get first candidate
        processor = await functions._determine_processor_optimal(source)  
        filtered_objects = await processor.extract_filtered_inventory(
            source, filters={}, details=interfaces.InventoryQueryDetails.Name
        )
        search_results = search.filter_by_name(
            filtered_objects, query,
            match_mode=interfaces.MatchMode.Fuzzy,
            fuzzy_threshold=50
        )
        obj = search_results[0].object
        
        print(f"Testing: {obj['name']}")
        print(f"URI: {obj['uri']}")
        
        # Step by step debugging
        base_url = _urls.normalize_base_url(source)
        doc_url = _urls.derive_documentation_url(base_url, obj['uri'], obj['name'])
        
        print(f"Doc URL: {doc_url.geturl()}")
        print(f"Fragment: {doc_url.fragment}")
        
        # Test HTTP retrieval
        try:
            from sphinxmcps.cacheproxy import retrieve_url_as_text
            html_content = await retrieve_url_as_text(doc_url)
            print(f"HTML content length: {len(html_content)}")
            print(f"HTML preview: {html_content[:200]}...")
        except Exception as e:
            print(f"HTTP error: {e}")
            return
            
        # Test HTML parsing
        anchor = doc_url.fragment or str(obj['name'])
        print(f"Using anchor: {anchor}")
        
        try:
            parsed_content = _extraction.parse_documentation_html(html_content, anchor)
            print(f"Parsing result keys: {parsed_content.keys()}")
            
            if 'error' in parsed_content:
                print(f"Parsing error: {parsed_content['error']}")
            else:
                print(f"Signature: {parsed_content.get('signature', 'NONE')[:100]}...")
                print(f"Description length: {len(parsed_content.get('description', ''))}")
                
        except Exception as e:
            print(f"Parsing exception: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    asyncio.run(debug_html_parsing())