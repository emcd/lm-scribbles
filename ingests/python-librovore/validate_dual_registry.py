#!/usr/bin/env python3

import asyncio
from librovore import xtnsapi
from librovore.inventories import register as inventory_register
from librovore.structures.sphinx import register
from librovore.structures.mkdocs import register as mkdocs_register

# Register processors like tests do
inventory_register({})
register({})
mkdocs_register({})

print('Inventory processors:', list(xtnsapi.inventory_processors.keys()))
print('Structure processors:', list(xtnsapi.structure_processors.keys()))

# Test detection
async def test_detection():
    from librovore.detection import detect_inventory, detect_structure
    
    # Test with a local test file
    test_file = '/home/me/src/python-librovore/tests/data/inventories/librovore/objects.inv'
    
    try:
        inv_detection = await detect_inventory(test_file)
        print(f'Inventory detection: {type(inv_detection).__name__} with confidence {inv_detection.confidence}')
    except Exception as e:
        print(f'Inventory detection failed: {e}')
    
    try:
        struct_detection = await detect_structure(test_file)
        print(f'Structure detection: {type(struct_detection).__name__} with confidence {struct_detection.confidence}')
    except Exception as e:
        print(f'Structure detection failed: {e}')

if __name__ == '__main__':
    asyncio.run(test_detection())