#!/usr/bin/env python3
"""
Quick test of the new MatchMode enum and fuzzy matching functionality.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'sources'))

from sphinxmcps.functions import extract_inventory, MatchMode

def test_match_modes():
    """Test different match modes with sphobjinv docs."""
    print("=== Testing MatchMode Implementation ===\n")
    
    source = "https://sphobjinv.readthedocs.io/en/stable/"
    
    # Test 1: Exact matching (default)
    print("1. Testing EXACT mode:")
    try:
        result = extract_inventory(source, term="Inventory", match_mode=MatchMode.EXACT)
        print(f"   Found {result['object_count']} objects")
        print(f"   Filters: {result.get('filters', 'None')}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 2: Regex matching  
    print("\n2. Testing REGEX mode:")
    try:
        result = extract_inventory(source, term="Inventor.*", match_mode=MatchMode.REGEX)
        print(f"   Found {result['object_count']} objects")
        print(f"   Filters: {result.get('filters', 'None')}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 3: Fuzzy matching
    print("\n3. Testing FUZZY mode:")
    
    # First, let's test what sphobjinv.suggest() returns directly
    print("   Debug: Testing sphobjinv.suggest() directly...")
    try:
        import sphobjinv
        inv = sphobjinv.Inventory(url=source + "objects.inv")
        suggestions = inv.suggest("Inventorry", thresh=50)
        print(f"   Direct suggest() returned: {suggestions[:5]}")
        
        # Try with lower threshold
        suggestions_low = inv.suggest("Inventorry", thresh=30)
        print(f"   Lower threshold (30): {suggestions_low[:5]}")
        
        # Try a different term
        suggestions_data = inv.suggest("DataObj", thresh=50)
        print(f"   'DataObj' suggest: {suggestions_data[:5]}")
    except Exception as e:
        print(f"   Direct suggest error: {e}")
    
    # Now test our implementation
    try:
        result = extract_inventory(source, term="DataObj", match_mode=MatchMode.FUZZY, fuzzy_threshold=50)
        print(f"   Our fuzzy 'DataObj' found {result['object_count']} objects")
        print(f"   Filters: {result.get('filters', 'None')}")
        # Show a few example matches
        if result['objects']:
            domain = list(result['objects'].keys())[0]
            examples = result['objects'][domain][:3]
            print(f"   Example matches: {[obj['name'] for obj in examples]}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test 4: Enum values
    print("\n4. Testing enum values:")
    print(f"   MatchMode.EXACT = {MatchMode.EXACT}")
    print(f"   MatchMode.REGEX = {MatchMode.REGEX}")
    print(f"   MatchMode.FUZZY = {MatchMode.FUZZY}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_match_modes()