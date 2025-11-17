#!/usr/bin/env python3

import sys
sys.path.insert(0, 'sources')

def test_cli_directly():
    """Test CLI parsing directly to see what's happening"""
    import tyro
    from sphinxmcps.cli import Cli
    
    # Simulate the command line args
    test_args = ['use', 'query-content']
    
    try:
        result = tyro.cli(Cli, args=test_args, return_unknown_args=False)
        print(f"CLI parsed successfully: {result}")
        print(f"Command type: {type(result.command)}")
        print(f"Command: {result.command}")
    except Exception as e:
        print(f"CLI parsing failed: {e}")
        print(f"Exception type: {type(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_cli_directly()