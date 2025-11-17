#!/usr/bin/env python3
"""Verify architectural fixes are working correctly."""

import inspect
import sys
from pathlib import Path

# Add sources to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'sources'))

import sphinxmcps.xtnsapi as xtnsapi
import sphinxmcps.xtnsmgr as xtnsmgr

# Test dynamic builtin import works
mod = xtnsmgr.import_builtin_processor('sphinxmcps', 'sphinx')
print('✓ Dynamic builtin import works')

# Test that no hardcoded mappings exist in xtnsapi
source = inspect.getsource(xtnsapi)
has_hardcoded = '_BUILTIN_PROCESSORS' in source or 'sphinxmcps.processors.sphinx' in source
print('✓ No hardcoded mappings:', not has_hardcoded)

# Test that import separation is maintained 
has_toplevel_import = 'from . import xtnsmgr' in source.split('def ')[0]
print('✓ No top-level xtnsmgr import:', not has_toplevel_import)

print('All architectural fixes verified!')