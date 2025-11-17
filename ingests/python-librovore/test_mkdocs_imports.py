#!/usr/bin/env python3

# Test the imports step by step
try:
    from librovore.inventories.mkdocs import __
    print('✓ MkDocs __ import successful')
    print('Available in __:', [attr for attr in dir(__) if not attr.startswith('_')])
except Exception as e:
    print('✗ MkDocs __ import failed:', e)
    import traceback
    traceback.print_exc()

try:
    from librovore.inventories.mkdocs.main import MkDocsInventoryProcessor
    print('✓ MkDocsInventoryProcessor import successful')
except Exception as e:
    print('✗ MkDocsInventoryProcessor import failed:', e)
    import traceback
    traceback.print_exc()