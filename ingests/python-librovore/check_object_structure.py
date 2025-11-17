#!/usr/bin/env python3

import sys
import asyncio
sys.path.insert(0, 'sources')

async def check_object_structure():
    """Check what fields are available in inventory objects"""
    from sphinxmcps import functions
    from sphinxmcps import xtnsmgr
    from sphinxmcps.cli import _prepare
    from sphinxmcps import interfaces
    import contextlib
    
    async with contextlib.AsyncExitStack() as exits:
        auxdata = await _prepare(environment=True, exits=exits, logfile=None)
        await xtnsmgr.register_processors(auxdata)
        
        source = '.auxiliary/artifacts/sphinx-html'
        
        # Get inventory objects
        processor = await functions._determine_processor_optimal(source)
        filtered_objects = await processor.extract_filtered_inventory(
            source, 
            filters={},
            details=interfaces.InventoryQueryDetails.Name
        )
        
        print(f"Total objects: {len(filtered_objects)}")
        print("\nFirst 3 objects and their keys:")
        for i, obj in enumerate(filtered_objects[:3]):
            print(f"\nObject {i+1}:")
            print(f"  Keys: {list(obj.keys())}")
            print(f"  Sample: {obj}")
        
        # Check if any objects have 'domain' key
        objects_with_domain = [obj for obj in filtered_objects if 'domain' in obj]
        print(f"\nObjects with 'domain' key: {len(objects_with_domain)}")
        
        if objects_with_domain:
            print("Sample object with domain:")
            print(f"  {objects_with_domain[0]}")
        
        # Check what domains are available  
        domain_values = set()
        for obj in filtered_objects:
            if 'domain' in obj:
                domain_values.add(obj['domain'])
        
        print(f"\nUnique domain values: {domain_values}")

if __name__ == '__main__':
    asyncio.run(check_object_structure())