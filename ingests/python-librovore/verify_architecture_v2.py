#!/usr/bin/env python3
"""Verify architectural fixes are working correctly."""

import inspect
import sys
from pathlib import Path

# Add sources to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'sources'))

import sphinxmcps.xtnsapi as xtnsapi
import sphinxmcps.xtnsmgr as xtnsmgr
import sphinxmcps.server as server
import sphinxmcps.cli as cli

print("🔍 Verifying Architectural Changes...")

# 1. Verify load_and_register_processors moved to xtnsmgr
has_load_in_xtnsmgr = hasattr(xtnsmgr, 'load_and_register_processors')
no_load_in_xtnsapi = not hasattr(xtnsapi, 'load_and_register_processors')
print('✓ load_and_register_processors in xtnsmgr:', has_load_in_xtnsmgr)
print('✓ load_and_register_processors NOT in xtnsapi:', no_load_in_xtnsapi)

# 2. Verify no xtnsmgr import in xtnsapi
xtnsapi_source = inspect.getsource(xtnsapi)
no_xtnsmgr_import = 'xtnsmgr' not in xtnsapi_source
print('✓ No xtnsmgr import in xtnsapi:', no_xtnsmgr_import)

# 3. Verify server doesn't load processors
server_source = inspect.getsource(server.serve)
no_processor_loading_in_server = 'load_and_register' not in server_source
print('✓ Server doesnt load processors:', no_processor_loading_in_server)

# 4. Verify CLI loads processors
cli_source = inspect.getsource(cli.Cli.__call__)
cli_loads_processors = 'xtnsmgr.load_and_register_processors' in cli_source
print('✓ CLI loads processors:', cli_loads_processors)

# 5. Verify no hardcoded fallbacks in processor loader
try:
    from sphinxmcps.xtnsmgr.processor_loader import load_and_register_processors
    loader_source = inspect.getsource(load_and_register_processors)
    no_hardcoded_fallback = 'processors.sphinx' not in loader_source
    has_warnings = 'warning' in loader_source.lower()
    print('✓ No hardcoded sphinx fallback:', no_hardcoded_fallback)
    print('✓ Has proper warnings:', has_warnings)
except ImportError:
    print('❌ Failed to import processor loader')

if all([
    has_load_in_xtnsmgr,
    no_load_in_xtnsapi, 
    no_xtnsmgr_import,
    no_processor_loading_in_server,
    cli_loads_processors,
    no_hardcoded_fallback,
    has_warnings
]):
    print('\n🎉 All architectural changes verified successfully!')
else:
    print('\n❌ Some architectural issues remain')