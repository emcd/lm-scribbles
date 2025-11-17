#!/usr/bin/env python3

import dataclasses as dcls
import sys
sys.path.insert(0, 'sources')
from sphinxmcps.interfaces import SearchBehaviors

# Test extracting fields from the immutable dataclass
def test_make_dataclass_approach():
    print("=== Testing make_dataclass approach ===")
    
    # Get fields from the immutable dataclass
    immutable_fields = dcls.fields(SearchBehaviors)
    print(f"Immutable fields: {[(f.name, f.type, f.default) for f in immutable_fields]}")
    
    # Convert to make_dataclass format
    field_specs = []
    for field in immutable_fields:
        if field.name.startswith('_'):
            continue  # Skip private fields
        
        # Build field spec: (name, type, default_value)
        if field.default != dcls.MISSING:
            field_specs.append((field.name, field.type, field.default))
        elif field.default_factory != dcls.MISSING:
            field_specs.append((field.name, field.type, dcls.field(default_factory=field.default_factory)))
        else:
            field_specs.append((field.name, field.type))
    
    print(f"Field specs for make_dataclass: {field_specs}")
    
    # Create the mutable dataclass
    SearchBehaviorsMutableDynamic = dcls.make_dataclass(
        'SearchBehaviorsMutableDynamic',
        field_specs,
        frozen=False  # Make it mutable
    )
    
    # Test it works
    instance = SearchBehaviorsMutableDynamic()
    print(f"Created instance: {instance}")
    print(f"Instance type: {type(instance)}")
    print(f"Instance fields: {[(f.name, getattr(instance, f.name)) for f in dcls.fields(instance)]}")
    
    # Test mutability
    instance.fuzzy_threshold = 75
    print(f"After mutation: {instance}")
    
    return SearchBehaviorsMutableDynamic

if __name__ == "__main__":
    SearchBehaviorsMutableDynamic = test_make_dataclass_approach()
    
    # Test JSON serialization behavior (what FastMCP/Pydantic cares about)
    instance = SearchBehaviorsMutableDynamic()
    print(f"\nDefault instance dict: {instance.__dict__}")
    
    # Check if this avoids the internal attribute leak
    print(f"Instance vars: {vars(instance)}")