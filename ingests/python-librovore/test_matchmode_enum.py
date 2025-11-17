#!/usr/bin/env python3
"""Test our actual MatchMode enum with Pydantic."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'sources'))

from pydantic import BaseModel, Field
import json
from sphinxmcps.interfaces import MatchMode

class TestModel(BaseModel):
    match_mode: MatchMode = Field(description="Term matching mode: 'exact', 'regex', or 'fuzzy'")

def main():
    print("=== Testing MatchMode Enum with Pydantic ===")
    
    # Test JSON schema generation
    print("\n1. JSON Schema:")
    schema = TestModel.model_json_schema()
    print(json.dumps(schema, indent=2))
    
    # Test serialization from enum
    print("\n2. Serialization from enum:")
    m1 = TestModel(match_mode=MatchMode.Fuzzy)
    print(f"Model: {m1}")
    print(f"JSON: {m1.model_dump_json()}")
    
    # Test deserialization from string
    print("\n3. Deserialization from string:")
    m2 = TestModel.model_validate({'match_mode': 'regex'})
    print(f"Model: {m2}")
    print(f"Enum value: {m2.match_mode}")
    print(f"Enum type: {type(m2.match_mode)}")
    print(f"Is MatchMode instance: {isinstance(m2.match_mode, MatchMode)}")
    
    # Test deserialization from invalid string
    print("\n4. Deserialization from invalid string:")
    try:
        m3 = TestModel.model_validate({'match_mode': 'invalid'})
        print(f"Model: {m3}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n5. All MatchMode values:")
    for mode in MatchMode:
        print(f"  {mode.name} = '{mode.value}'")

if __name__ == "__main__":
    main()