#!/usr/bin/env python3

import sys
import asyncio
sys.path.insert(0, 'sources')

async def test_theme_detection():
    """Test theme detection for various sites"""
    from sphinxmcps import functions
    from sphinxmcps import xtnsmgr
    from sphinxmcps.cli import _prepare
    import contextlib
    
    async with contextlib.AsyncExitStack() as exits:
        auxdata = await _prepare(environment=True, exits=exits, logfile=None)
        await xtnsmgr.register_processors(auxdata)
        
        test_sites = [
            ('.auxiliary/artifacts/sphinx-html', 'Local site'),
            ('https://docs.python.org/3/', 'Python docs'),
            ('https://flask.palletsprojects.com/en/stable/', 'Flask docs'),
        ]
        
        for source, name in test_sites:
            print(f"\n=== {name} ===")
            try:
                processor = await functions._determine_processor_optimal(source)
                detection = await processor.detect(source)
                
                print(f"Source: {source}")
                print(f"Confidence: {detection.confidence}")
                print(f"Theme: {getattr(detection, 'theme', 'Not available')}")
                print(f"Has objects.inv: {getattr(detection, 'has_objects_inv', 'Unknown')}")
                print(f"Has searchindex: {getattr(detection, 'has_searchindex', 'Unknown')}")
                
            except Exception as e:
                print(f"Error: {e}")

if __name__ == '__main__':
    asyncio.run(test_theme_detection())