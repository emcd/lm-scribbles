#!/usr/bin/env python3

"""Test to determine when ABC attributes are set during class lifecycle."""

import sys
print(f"Python implementation: {sys.implementation.name}")

from typing import Protocol, runtime_checkable

def show_abc_attrs(cls, stage):
    """Show current ABC attributes on a class."""
    abc_attrs = {attr: getattr(cls, attr, '<MISSING>')
                 for attr in ['_abc_cache', '_abc_negative_cache', '_abc_negative_cache_version', '_abc_registry']
                 if hasattr(cls, attr)}
    print(f"{stage}: {abc_attrs}")

# Test 1: Protocol class creation lifecycle
print("\n=== Test 1: Protocol class creation ===")

print("Before class definition:")

@runtime_checkable
class TestProtocol(Protocol):
    print("During class body execution:")
    # This runs during class creation
    show_abc_attrs(locals(), "  Inside class body")

    def test_method(self) -> str: ...

print("After class definition:")
show_abc_attrs(TestProtocol, "  After @runtime_checkable")

# Test 2: First isinstance call (should trigger lazy initialization)
print("\n=== Test 2: First isinstance call ===")

class ImplementsProtocol:
    def test_method(self) -> str:
        return "implemented"

print("Before first isinstance:")
show_abc_attrs(TestProtocol, "  Before isinstance")

print("Calling isinstance(ImplementsProtocol(), TestProtocol)...")
result1 = isinstance(ImplementsProtocol(), TestProtocol)
print(f"Result: {result1}")

print("After first isinstance:")
show_abc_attrs(TestProtocol, "  After first isinstance")

# Test 3: Negative isinstance call (should populate negative cache)
print("\n=== Test 3: Negative isinstance call ===")

class DoesNotImplement:
    def other_method(self) -> None:
        pass

print("Before negative isinstance:")
show_abc_attrs(TestProtocol, "  Before negative isinstance")

print("Calling isinstance(DoesNotImplement(), TestProtocol)...")
result2 = isinstance(DoesNotImplement(), TestProtocol)
print(f"Result: {result2}")

print("After negative isinstance:")
show_abc_attrs(TestProtocol, "  After negative isinstance")

# Test 4: Multiple isinstance calls to see cache behavior
print("\n=== Test 4: Cache behavior with repeated calls ===")

print("Before repeated calls:")
show_abc_attrs(TestProtocol, "  Before repeated calls")

# Call same isinstance multiple times
for i in range(3):
    isinstance(DoesNotImplement(), TestProtocol)
    isinstance(ImplementsProtocol(), TestProtocol)

print("After repeated calls:")
show_abc_attrs(TestProtocol, "  After repeated calls")

# Test 5: Manual cache inspection
print("\n=== Test 5: Cache contents inspection ===")
if hasattr(TestProtocol, '_abc_negative_cache'):
    print(f"Negative cache contents: {TestProtocol._abc_negative_cache}")
if hasattr(TestProtocol, '_abc_cache'):
    print(f"Positive cache contents: {TestProtocol._abc_cache}")
if hasattr(TestProtocol, '_abc_registry'):
    print(f"Registry contents: {TestProtocol._abc_registry}")

# Test 6: Check if we can trigger cache mutation after class creation
print("\n=== Test 6: Can we trigger post-creation mutations? ===")

class NewClass:
    def test_method(self) -> str:
        return "new"

print("Testing with a brand new class:")
show_abc_attrs(TestProtocol, "  Before new class test")

result3 = isinstance(NewClass(), TestProtocol)
print(f"isinstance(NewClass(), TestProtocol): {result3}")

print("After new class test:")
show_abc_attrs(TestProtocol, "  After new class test")

# Test 7: What happens with subclass registration?
print("\n=== Test 7: Subclass registration ===")
if hasattr(TestProtocol, 'register'):
    print("Attempting to register a class...")

    class ToRegister:
        def test_method(self) -> str:
            return "registered"

    print("Before registration:")
    show_abc_attrs(TestProtocol, "  Before register()")

    TestProtocol.register(ToRegister)

    print("After registration:")
    show_abc_attrs(TestProtocol, "  After register()")

    print(f"isinstance(ToRegister(), TestProtocol): {isinstance(ToRegister(), TestProtocol)}")

print("\n=== Summary ===")
print("This should show us exactly when each ABC attribute gets populated!")