#!/usr/bin/env python3

import sys
sys.path.insert(0, 'sources')

def test_cli_execution():
    """Test the actual CLI execution path"""
    import asyncio
    import tyro
    from sphinxmcps.cli import Cli
    
    # Test the exact same pattern as execute()
    config = (
        tyro.conf.HelptextFromCommentsOff,
    )
    
    # Simulate missing arguments
    test_args = ['use', 'query-content']
    
    try:
        # This should fail at the tyro.cli level before asyncio.run
        cli_instance = tyro.cli(Cli, config=config, args=test_args)
        print(f"CLI instance created: {cli_instance}")
        
        # Now try to run it
        asyncio.run(cli_instance())
        
    except SystemExit as e:
        print(f"SystemExit caught with code: {e.code}")
        raise
    except Exception as e:
        print(f"Other exception: {e}")
        raise

if __name__ == '__main__':
    test_cli_execution()