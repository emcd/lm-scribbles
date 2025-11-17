#!/usr/bin/env python3
"""
Test script to debug dataclasses.fields() approach with FiltersMutable.
"""

import dataclasses
import sys
import traceback

# Add the project to the path so we can import our modules
sys.path.insert(0, 'sources')

from sphinxmcps import interfaces
from sphinxmcps.server import FiltersMutable

def test_explicit_approach():
    """Test the current explicit conversion approach."""
    print("=== Testing Explicit Approach ===")
    try:
        # Create a mutable filter
        mutable_filters = FiltersMutable(
            domain="py",
            role="class", 
            priority="1",
            match_mode=interfaces.MatchMode.Fuzzy,
            fuzzy_threshold=80
        )
        print(f"Mutable filters: {mutable_filters}")
        
        # Convert using explicit approach
        immutable_filters = interfaces.Filters(
            domain=mutable_filters.domain,
            role=mutable_filters.role,
            priority=mutable_filters.priority,
            match_mode=mutable_filters.match_mode,
            fuzzy_threshold=mutable_filters.fuzzy_threshold
        )
        print(f"Immutable filters: {immutable_filters}")
        print("✅ Explicit approach works!")
        return True
        
    except Exception as exc:
        print(f"❌ Explicit approach failed: {exc}")
        traceback.print_exc()
        return False

def test_dataclasses_fields_approach():
    """Test the dataclasses.fields() approach."""
    print("\n=== Testing dataclasses.fields() Approach ===")
    try:
        # Create a mutable filter
        mutable_filters = FiltersMutable(
            domain="py",
            role="class",
            priority="1", 
            match_mode=interfaces.MatchMode.Fuzzy,
            fuzzy_threshold=80
        )
        print(f"Mutable filters: {mutable_filters}")
        
        # Check if it's a dataclass
        print(f"Is dataclass: {dataclasses.is_dataclass(mutable_filters)}")
        
        # Get fields
        fields = dataclasses.fields(mutable_filters)
        print(f"Fields: {[field.name for field in fields]}")
        
        # Extract field values, filtering out frigid internal fields
        field_values = {
            field.name: getattr(mutable_filters, field.name)
            for field in fields
            if not field.name.startswith('_frigid_')
        }
        print(f"Field values (filtered): {field_values}")
        
        # Convert using dataclasses.fields approach
        immutable_filters = interfaces.Filters(**field_values)
        print(f"Immutable filters: {immutable_filters}")
        print("✅ dataclasses.fields() approach works!")
        return True
        
    except Exception as exc:
        print(f"❌ dataclasses.fields() approach failed: {exc}")
        traceback.print_exc()
        return False

def test_frigid_compatibility():
    """Test frigid objects compatibility with dataclasses."""
    print("\n=== Testing Frigid Compatibility ===")
    try:
        # Test regular Filters object
        regular_filters = interfaces.Filters()
        print(f"Regular filters: {regular_filters}")
        print(f"Regular is dataclass: {dataclasses.is_dataclass(regular_filters)}")
        
        # Test mutable filters
        mutable_filters = FiltersMutable()
        print(f"Mutable filters: {mutable_filters}")
        print(f"Mutable is dataclass: {dataclasses.is_dataclass(mutable_filters)}")
        
        # Try to get fields from both
        if dataclasses.is_dataclass(regular_filters):
            regular_fields = dataclasses.fields(regular_filters)
            print(f"Regular fields: {[f.name for f in regular_fields]}")
        
        if dataclasses.is_dataclass(mutable_filters):
            mutable_fields = dataclasses.fields(mutable_filters)
            print(f"Mutable fields: {[f.name for f in mutable_fields]}")
            
        print("✅ Frigid compatibility test passed!")
        return True
        
    except Exception as exc:
        print(f"❌ Frigid compatibility test failed: {exc}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing FiltersMutable and dataclasses.fields() compatibility\n")
    
    results = []
    results.append(test_explicit_approach())
    results.append(test_dataclasses_fields_approach()) 
    results.append(test_frigid_compatibility())
    
    print(f"\n=== Summary ===")
    print(f"Explicit approach: {'✅' if results[0] else '❌'}")
    print(f"dataclasses.fields() approach: {'✅' if results[1] else '❌'}")
    print(f"Frigid compatibility: {'✅' if results[2] else '❌'}")
    
    if all(results):
        print("\n🎉 All tests passed! dataclasses.fields() should work.")
    else:
        print("\n⚠️  Some tests failed. Check the error messages above.")