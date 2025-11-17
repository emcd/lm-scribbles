#!/usr/bin/env python3

from librovore import xtnsapi
from librovore.xtnsmgr import processors, configuration
from appcore.state import Globals
import asyncio

async def test_config():
    # Create mock globals with our config
    globals_obj = Globals()
    globals_obj.configuration = {
        'inventory-extensions': [{'name': 'sphinx', 'enabled': True}],
        'structure-extensions': [
            {'name': 'sphinx', 'enabled': True},
            {'name': 'mkdocs', 'enabled': True}
        ]
    }
    
    print('Testing configuration extraction...')
    inv_ext = configuration.extract_inventory_extensions(globals_obj)
    struct_ext = configuration.extract_structure_extensions(globals_obj)
    
    print(f'Inventory extensions: {[e["name"] for e in inv_ext]}')
    print(f'Structure extensions: {[e["name"] for e in struct_ext]}')
    
    print('\nTesting processor registration...')
    await processors.register_processors(globals_obj)
    
    print(f'Registered inventory processors: {list(xtnsapi.inventory_processors.keys())}')
    print(f'Registered structure processors: {list(xtnsapi.structure_processors.keys())}')

if __name__ == '__main__':
    asyncio.run(test_config())