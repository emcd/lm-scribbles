#!/usr/bin/env python3

"""Test to see exactly when ABC cache objects get mutated internally."""

import sys
print(f"Python implementation: {sys.implementation.name}")

from typing import Protocol, runtime_checkable

def inspect_cache_detailed(cls, stage):
    """Detailed inspection of cache object contents."""
    print(f"\n{stage}:")

    for attr_name in ['_abc_cache', '_abc_negative_cache', '_abc_registry']:
        if hasattr(cls, attr_name):
            cache_obj = getattr(cls, attr_name)
            # Try to get length/contents of cache objects
            try:
                # WeakSet objects have data attribute
                if hasattr(cache_obj, 'data'):
                    contents = list(cache_obj.data)
                    print(f"  {attr_name}: {len(contents)} items: {contents}")
                elif hasattr(cache_obj, '__len__'):
                    print(f"  {attr_name}: length {len(cache_obj)}")
                else:
                    print(f"  {attr_name}: {cache_obj}")
            except Exception as e:
                print(f"  {attr_name}: <inspection failed: {e}>")

    if hasattr(cls, '_abc_negative_cache_version'):
        version = getattr(cls, '_abc_negative_cache_version')
        print(f"  _abc_negative_cache_version: {version}")

@runtime_checkable
class TestProtocol(Protocol):
    def test_method(self) -> str: ...

inspect_cache_detailed(TestProtocol, "After class creation")

# Test with classes that definitely don't implement the protocol
class DefinitelyNot:
    pass

class AlsoNot:
    def wrong_method(self): pass

print("\n=== Testing isinstance with non-implementing classes ===")

print("First isinstance call...")
result1 = isinstance(DefinitelyNot(), TestProtocol)
print(f"isinstance(DefinitelyNot(), TestProtocol): {result1}")
inspect_cache_detailed(TestProtocol, "After first negative isinstance")

print("Second isinstance call...")
result2 = isinstance(AlsoNot(), TestProtocol)
print(f"isinstance(AlsoNot(), TestProtocol): {result2}")
inspect_cache_detailed(TestProtocol, "After second negative isinstance")

# Test with implementing classes
class Implements1:
    def test_method(self) -> str:
        return "impl1"

class Implements2:
    def test_method(self) -> str:
        return "impl2"

print("\n=== Testing isinstance with implementing classes ===")

print("First positive isinstance...")
result3 = isinstance(Implements1(), TestProtocol)
print(f"isinstance(Implements1(), TestProtocol): {result3}")
inspect_cache_detailed(TestProtocol, "After first positive isinstance")

print("Second positive isinstance...")
result4 = isinstance(Implements2(), TestProtocol)
print(f"isinstance(Implements2(), TestProtocol): {result4}")
inspect_cache_detailed(TestProtocol, "After second positive isinstance")

# Test registration
print("\n=== Testing explicit registration ===")

class ToRegister:
    pass

print("Before registration:")
inspect_cache_detailed(TestProtocol, "Before register()")

TestProtocol.register(ToRegister)
print("After registration:")
inspect_cache_detailed(TestProtocol, "After register()")

result5 = isinstance(ToRegister(), TestProtocol)
print(f"isinstance(ToRegister(), TestProtocol): {result5}")
inspect_cache_detailed(TestProtocol, "After isinstance on registered class")

print("\n=== Trying to trigger cache version changes ===")

# Try to manipulate caches to trigger version updates
import gc
print("Triggering garbage collection...")
gc.collect()
inspect_cache_detailed(TestProtocol, "After gc.collect()")

# Try clearing weak references by deleting objects
del DefinitelyNot, AlsoNot, Implements1, Implements2
gc.collect()
inspect_cache_detailed(TestProtocol, "After deleting test classes and gc")

print("\n=== Summary ===")
print("This should reveal if cache contents change during isinstance operations!")