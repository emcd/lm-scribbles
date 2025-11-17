#!/usr/bin/env python3
print("Testing whether NotImplementedError is coming from missing CLI methods...")

# Try to understand where the NotImplementedError is coming from by testing step by step
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../sources'))

try:
    from librovore.cli import DetectCommand
    print("✅ DetectCommand imported successfully")

    # Check if the method exists
    cmd = DetectCommand(location="https://test.example", genus="Inventory")
    print("✅ DetectCommand instantiated successfully")

    if hasattr(cmd, '__call__'):
        print("✅ DetectCommand has __call__ method")
    else:
        print("❌ DetectCommand missing __call__ method")

    if hasattr(cmd, 'execute'):
        print("✅ DetectCommand has execute method")
    else:
        print("⚠️ DetectCommand does not have execute method")

except Exception as e:
    print(f"❌ Error importing/testing: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()