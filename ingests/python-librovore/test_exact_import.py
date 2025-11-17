#!/usr/bin/env python3

# Test the exact import pattern used by the registration system
import sys
import importlib

module_name = "librovore.inventories.mkdocs"
print(f"Attempting to import: {module_name}")

try:
    module = importlib.import_module(module_name)
    print(f"✓ Successfully imported: {module_name}")
    
    # Check if it has a register function
    if hasattr(module, 'register'):
        print("✓ Found register function")
        try:
            module.register({})
            print("✓ Registration completed successfully")
        except Exception as e:
            print(f"✗ Registration failed: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("✗ No register function found")
        print("Available attributes:", [attr for attr in dir(module) if not attr.startswith('_')])
        
except Exception as e:
    print(f"✗ Import failed: {e}")
    import traceback
    traceback.print_exc()