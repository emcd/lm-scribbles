#!/usr/bin/env python3

import asyncio
from librovore import cli
from librovore.xtnsmgr import configuration

async def test_config():
    # Simulate CLI preparation
    import librovore.__ as __
    import contextlib
    
    async with contextlib.AsyncExitStack() as exits:
        auxdata = await cli._prepare(
            environment=True,
            exits=exits,
            logfile=None
        )
        
        print("Configuration object:", auxdata.configuration)
        if auxdata.configuration:
            print("Extensions in config:", auxdata.configuration.get('extensions', 'NOT FOUND'))
        
        try:
            extensions = configuration.extract_extensions(auxdata)
            print("Extracted extensions:", extensions)
            
            active = configuration.select_active_extensions(extensions)
            print("Active extensions:", active)
            
            intrinsic = configuration.select_intrinsic_extensions(active)
            print("Intrinsic extensions:", intrinsic)
            
        except Exception as e:
            print("Error extracting extensions:", e)

if __name__ == '__main__':
    asyncio.run(test_config())