#!/usr/bin/env python3

"""Test to discover what ABC cache attributes PyPy needs to set on protocol classes."""

import sys
print(f"Python implementation: {sys.implementation.name}")
print(f"Python version: {sys.version}")

from typing import Protocol, runtime_checkable
import abc

# Create a simple protocol to test ABC behavior
@runtime_checkable
class TestProtocol(Protocol):
    def test_method(self) -> str: ...

# Create a class that might implement the protocol
class ImplementsProtocol:
    def test_method(self) -> str:
        return "implemented"

# Create a class that doesn't implement the protocol
class DoesNotImplement:
    def other_method(self) -> None:
        pass

print("\n=== Testing ABC cache behavior ===")

# Before any isinstance checks, inspect what attributes exist
print(f"\nBefore isinstance checks:")
print(f"TestProtocol.__dict__ keys: {sorted(TestProtocol.__dict__.keys())}")

# Look for any ABC-related attributes
abc_attrs = [attr for attr in TestProtocol.__dict__.keys() if '_abc' in attr.lower()]
print(f"Existing ABC attributes: {abc_attrs}")

# Now do isinstance checks that should trigger cache creation
print(f"\n=== Running isinstance checks ===")

try:
    result1 = isinstance(ImplementsProtocol(), TestProtocol)
    print(f"isinstance(ImplementsProtocol(), TestProtocol): {result1}")
except Exception as e:
    print(f"ERROR during positive isinstance check: {e}")

try:
    result2 = isinstance(DoesNotImplement(), TestProtocol)
    print(f"isinstance(DoesNotImplement(), TestProtocol): {result2}")
except Exception as e:
    print(f"ERROR during negative isinstance check: {e}")

# Check what attributes were added
print(f"\nAfter isinstance checks:")
print(f"TestProtocol.__dict__ keys: {sorted(TestProtocol.__dict__.keys())}")

# Look for new ABC-related attributes
new_abc_attrs = [attr for attr in TestProtocol.__dict__.keys() if '_abc' in attr.lower()]
print(f"ABC attributes after checks: {new_abc_attrs}")

# Try to manually inspect what attributes ABC might want to set
print(f"\n=== Manual ABC inspection ===")

# Check what abc module attributes look like
print(f"dir(abc): {[attr for attr in dir(abc) if 'cache' in attr.lower()]}")

# Check if there are any ABC-related attributes on typing.Protocol
print(f"typing.Protocol ABC attrs: {[attr for attr in dir(Protocol) if '_abc' in attr.lower()]}")

# Also test with collections.abc.Mapping to see standard ABC behavior
from collections.abc import Mapping

print(f"\n=== Testing standard ABC (collections.abc.Mapping) ===")
print(f"Before isinstance: Mapping ABC attrs: {[attr for attr in Mapping.__dict__.keys() if '_abc' in attr.lower()]}")

# Test isinstance with Mapping
test_dict = {"key": "value"}
test_list = [1, 2, 3]

try:
    mapping_result1 = isinstance(test_dict, Mapping)
    print(f"isinstance(dict, Mapping): {mapping_result1}")
except Exception as e:
    print(f"ERROR with Mapping positive check: {e}")

try:
    mapping_result2 = isinstance(test_list, Mapping)
    print(f"isinstance(list, Mapping): {mapping_result2}")
except Exception as e:
    print(f"ERROR with Mapping negative check: {e}")

print(f"After isinstance: Mapping ABC attrs: {[attr for attr in Mapping.__dict__.keys() if '_abc' in attr.lower()]}")

# Try some edge cases that might reveal more cache attributes
print(f"\n=== Edge case testing ===")

# Multiple isinstance calls to see if behavior changes
for i in range(3):
    try:
        isinstance(DoesNotImplement(), TestProtocol)
    except Exception as e:
        print(f"Iteration {i+1} error: {e}")
        break
else:
    print("Multiple isinstance calls completed successfully")

print(f"Final TestProtocol ABC attrs: {[attr for attr in TestProtocol.__dict__.keys() if '_abc' in attr.lower()]}")