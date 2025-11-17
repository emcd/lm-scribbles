#!/usr/bin/env python3

# Test various import paths
try:
    import librovore
    print('✓ librovore imported')
except Exception as e:
    print('✗ librovore import failed:', e)

try:
    import librovore.inventories
    print('✓ librovore.inventories imported')
except Exception as e:
    print('✗ librovore.inventories import failed:', e)

try:
    import librovore.inventories.mkdocs
    print('✓ librovore.inventories.mkdocs imported')
except Exception as e:
    print('✗ librovore.inventories.mkdocs import failed:', e)

try:
    import librovore.inventories.sphinx
    print('✓ librovore.inventories.sphinx imported')
except Exception as e:
    print('✗ librovore.inventories.sphinx import failed:', e)