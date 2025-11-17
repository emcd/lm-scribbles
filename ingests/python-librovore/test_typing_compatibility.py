#!/usr/bin/env python3

import dataclasses as dcls
import sys
sys.path.insert(0, 'sources')
from sphinxmcps.interfaces import SearchBehaviors, MatchMode

def create_mutable_search_behaviors():
    """Create a mutable version of SearchBehaviors using make_dataclass."""
    # Get fields from the immutable dataclass
    immutable_fields = dcls.fields(SearchBehaviors)
    
    # Convert to make_dataclass format, filtering out private fields
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
    
    return dcls.make_dataclass(
        'SearchBehaviorsMutable',
        field_specs,
        frozen=False
    )

# Test type checking scenarios
def test_typing():
    SearchBehaviorsMutable = create_mutable_search_behaviors()
    
    # Test instantiation
    instance = SearchBehaviorsMutable()
    print(f"Default instance: {instance}")
    
    # Test with explicit values
    explicit = SearchBehaviorsMutable(
        match_mode=MatchMode.Exact,
        fuzzy_threshold=80
    )
    print(f"Explicit instance: {explicit}")
    
    # Test field access
    print(f"Match mode: {instance.match_mode}")
    print(f"Fuzzy threshold: {instance.fuzzy_threshold}")
    
    # Test mutation
    instance.match_mode = MatchMode.Regex
    instance.fuzzy_threshold = 90
    print(f"After mutation: {instance}")
    
    # Test that it has proper dataclass features
    print(f"Is dataclass: {dcls.is_dataclass(instance)}")
    print(f"Fields: {[f.name for f in dcls.fields(instance)]}")
    
    return SearchBehaviorsMutable

if __name__ == "__main__":
    SearchBehaviorsMutable = test_typing()
    print(f"Generated class: {SearchBehaviorsMutable}")
    print(f"Class name: {SearchBehaviorsMutable.__name__}")
    print(f"Class annotations: {getattr(SearchBehaviorsMutable, '__annotations__', {})}")