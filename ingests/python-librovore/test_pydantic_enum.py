#!/usr/bin/env python3
"""Test how Pydantic handles enums in MCP context."""

from pydantic import BaseModel, Field
from enum import Enum
import json

class TestEnum(str, Enum):
    A = 'a'
    B = 'b'
    C = 'c'

class TestModel(BaseModel):
    value: TestEnum = Field(description='Test enum')

def main():
    print("=== Testing Pydantic Enum Handling ===")
    
    # Test JSON schema generation
    print("\n1. JSON Schema:")
    schema = TestModel.model_json_schema()
    print(json.dumps(schema, indent=2))
    
    # Test serialization from enum
    print("\n2. Serialization from enum:")
    m1 = TestModel(value=TestEnum.A)
    print(f"Model: {m1}")
    print(f"JSON: {m1.model_dump_json()}")
    print(f"Dict: {m1.model_dump()}")
    
    # Test deserialization from string
    print("\n3. Deserialization from string:")
    m2 = TestModel.model_validate({'value': 'b'})
    print(f"Model: {m2}")
    print(f"Enum value: {m2.value}")
    print(f"Enum type: {type(m2.value)}")
    print(f"Is enum instance: {isinstance(m2.value, TestEnum)}")
    
    # Test deserialization from invalid string
    print("\n4. Deserialization from invalid string:")
    try:
        m3 = TestModel.model_validate({'value': 'invalid'})
        print(f"Model: {m3}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test FastMCP-like function signature
    print("\n5. Test function signature with enum:")
    
    def test_function(
        value: TestEnum = Field(description="Test enum parameter")
    ) -> str:
        return f"Received: {value} (type: {type(value)})"
    
    # Simulate what FastMCP would do
    import inspect
    sig = inspect.signature(test_function)
    param = sig.parameters['value']
    print(f"Parameter annotation: {param.annotation}")
    print(f"Parameter default: {param.default}")
    
    # Test direct call
    result = test_function(TestEnum.B)
    print(f"Direct call result: {result}")

if __name__ == "__main__":
    main()