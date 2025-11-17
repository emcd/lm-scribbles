#!/usr/bin/env python3

import sys
sys.path.insert(0, 'sources')

def test_import():
    """Test if retrieve_url_as_text is available via __ import"""
    
    # Test the import chain
    print("Testing import chain...")
    
    try:
        from sphinxmcps.processors.sphinx import __
        print("✅ Successfully imported sphinxmcps.processors.sphinx.__")
        
        # Check if the function is available
        if hasattr(__, 'retrieve_url_as_text'):
            print("✅ retrieve_url_as_text is available in __")
            print(f"   Function: {__.retrieve_url_as_text}")
        else:
            print("❌ retrieve_url_as_text is NOT available in __")
            print(f"   Available attributes: {[attr for attr in dir(__) if 'retrieve' in attr.lower()]}")
            
    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_import()