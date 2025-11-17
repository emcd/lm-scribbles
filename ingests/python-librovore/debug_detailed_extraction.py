#!/usr/bin/env python3

import sys
import asyncio
sys.path.insert(0, 'sources')

async def debug_detailed_extraction():
    """Debug each step of documentation extraction"""
    from sphinxmcps import functions
    from sphinxmcps import xtnsmgr
    from sphinxmcps.cli import _prepare
    from sphinxmcps import search
    from sphinxmcps import interfaces
    from sphinxmcps.processors.sphinx import urls as _urls
    from sphinxmcps.processors.sphinx import extraction as _extraction
    from sphinxmcps.processors.sphinx import conversion as _conversion
    from sphinxmcps import __ as __
    from sphinxmcps import cacheproxy 
    import contextlib
    
    async with contextlib.AsyncExitStack() as exits:
        auxdata = await _prepare(environment=True, exits=exits, logfile=None)
        await xtnsmgr.register_processors(auxdata)
        
        source = '.auxiliary/artifacts/sphinx-html'
        
        # Get a test object
        processor = await functions._determine_processor_optimal(source)
        filtered_objects = await processor.extract_filtered_inventory(
            source, 
            filters={},
            details=interfaces.InventoryQueryDetails.Name
        )
        
        # Find an object with a normal URI
        normal_objects = [obj for obj in filtered_objects if not obj['uri'].endswith('#$')]
        if not normal_objects:
            print("No objects with normal URIs found!")
            return
            
        test_obj = normal_objects[0]
        print(f"Testing with object: {test_obj}")
        print()
        
        # Step 1: URL derivation
        try:
            base_url = _urls.normalize_base_url(source)
            print(f"Base URL: {base_url}")
            
            doc_url = _urls.derive_documentation_url(
                base_url, test_obj['uri'], test_obj['name']
            )
            print(f"Derived doc URL: {doc_url}")
            print(f"URL fragment: {doc_url.fragment}")
        except Exception as e:
            print(f"URL derivation failed: {e}")
            import traceback
            traceback.print_exc()
            return
        
        # Step 2: HTML retrieval
        try:
            html_content = await cacheproxy.retrieve_url_as_text(doc_url)
            print(f"Retrieved HTML content: {len(html_content)} characters")
            print(f"HTML preview: {html_content[:200]}...")
        except Exception as e:
            print(f"HTML retrieval failed: {e}")
            import traceback
            traceback.print_exc()
            return
        
        # Step 3: HTML parsing
        try:
            anchor = doc_url.fragment or str(test_obj['name'])
            print(f"Using anchor: '{anchor}'")
            
            parsed_content = _extraction.parse_documentation_html(
                html_content, anchor
            )
            print(f"Parsed content keys: {list(parsed_content.keys())}")
            if 'error' in parsed_content:
                print(f"Parse error: {parsed_content['error']}")
            else:
                print(f"Signature: {parsed_content.get('signature', 'N/A')}")
                print(f"Description: {parsed_content.get('description', 'N/A')[:100]}...")
        except Exception as e:
            print(f"HTML parsing failed: {e}")
            import traceback
            traceback.print_exc()
            return
        
        # Step 4: Markdown conversion
        if 'error' not in parsed_content:
            try:
                description = _conversion.html_to_markdown(
                    parsed_content['description']
                )
                print(f"Markdown description: {description[:100]}...")
            except Exception as e:
                print(f"Markdown conversion failed: {e}")
                import traceback
                traceback.print_exc()

if __name__ == '__main__':
    asyncio.run(debug_detailed_extraction())