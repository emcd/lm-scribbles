#!/usr/bin/env python3

"""Test to see if PyPy replaces ABC cache attributes vs just mutating their contents."""

import sys
print(f"Python implementation: {sys.implementation.name}")

from typing import Protocol, runtime_checkable

@runtime_checkable
class TestProtocol(Protocol):
    def test_method(self) -> str: ...

# Capture initial object identities
initial_cache = id(TestProtocol._abc_cache) if hasattr(TestProtocol, '_abc_cache') else None
initial_negative_cache = id(TestProtocol._abc_negative_cache) if hasattr(TestProtocol, '_abc_negative_cache') else None
initial_registry = id(TestProtocol._abc_registry) if hasattr(TestProtocol, '_abc_registry') else None
initial_version = TestProtocol._abc_negative_cache_version if hasattr(TestProtocol, '_abc_negative_cache_version') else None

print(f"Initial object IDs:")
print(f"  _abc_cache: {initial_cache}")
print(f"  _abc_negative_cache: {initial_negative_cache}")
print(f"  _abc_registry: {initial_registry}")
print(f"  _abc_negative_cache_version: {initial_version}")

def check_object_identity_changes(stage):
    """Check if the ABC attribute objects themselves changed."""
    print(f"\n{stage}:")

    current_cache = id(TestProtocol._abc_cache) if hasattr(TestProtocol, '_abc_cache') else None
    current_negative_cache = id(TestProtocol._abc_negative_cache) if hasattr(TestProtocol, '_abc_negative_cache') else None
    current_registry = id(TestProtocol._abc_registry) if hasattr(TestProtocol, '_abc_registry') else None
    current_version = TestProtocol._abc_negative_cache_version if hasattr(TestProtocol, '_abc_negative_cache_version') else None

    print(f"  _abc_cache: {current_cache} {'(CHANGED!)' if current_cache != initial_cache else '(same)'}")
    print(f"  _abc_negative_cache: {current_negative_cache} {'(CHANGED!)' if current_negative_cache != initial_negative_cache else '(same)'}")
    print(f"  _abc_registry: {current_registry} {'(CHANGED!)' if current_registry != initial_registry else '(same)'}")
    print(f"  _abc_negative_cache_version: {current_version} {'(CHANGED!)' if current_version != initial_version else '(same)'}")

# Test various operations that might trigger attribute replacement
class TestClass1:
    pass

class TestClass2:
    def test_method(self) -> str:
        return "impl"

print("\n=== Test 1: Simple isinstance calls ===")
isinstance(TestClass1(), TestProtocol)  # Should add to negative cache
check_object_identity_changes("After negative isinstance")

isinstance(TestClass2(), TestProtocol)  # Should add to positive cache
check_object_identity_changes("After positive isinstance")

print("\n=== Test 2: Registration ===")
class ToRegister:
    pass

TestProtocol.register(ToRegister)
check_object_identity_changes("After register()")

isinstance(ToRegister(), TestProtocol)  # This should clear negative cache
check_object_identity_changes("After isinstance on registered class")

print("\n=== Test 3: Cache invalidation scenarios ===")

# Try to trigger various cache invalidation scenarios
import gc

# Delete registered class to see if that triggers cache replacement
del ToRegister
gc.collect()
check_object_identity_changes("After deleting registered class")

# Multiple isinstance with new classes
for i in range(5):
    exec(f"""
class TempClass{i}:
    pass
isinstance(TempClass{i}(), TestProtocol)
""")

check_object_identity_changes("After multiple isinstance calls")

print("\n=== Test 4: Direct cache manipulation (if possible) ===")

# Try direct cache operations that might trigger replacement
try:
    if hasattr(TestProtocol, '_abc_negative_cache'):
        cache = TestProtocol._abc_negative_cache
        print(f"Cache type: {type(cache)}")
        print(f"Cache methods: {[m for m in dir(cache) if not m.startswith('_')]}")

        # Try clearing the cache directly
        if hasattr(cache, 'clear'):
            cache.clear()
            check_object_identity_changes("After cache.clear()")

        if hasattr(cache, 'data'):
            original_data_id = id(cache.data)
            print(f"Cache data ID before: {original_data_id}")

            # Force some operation that might replace data
            isinstance(TestClass1(), TestProtocol)

            new_data_id = id(cache.data)
            print(f"Cache data ID after: {new_data_id} {'(CHANGED!)' if new_data_id != original_data_id else '(same)'}")

except Exception as e:
    print(f"Cache manipulation error: {e}")

check_object_identity_changes("Final state")

print("\n=== Test 5: Attribute descriptor behavior ===")

# Check if these are descriptors that might do replacement
for attr_name in ['_abc_cache', '_abc_negative_cache', '_abc_registry']:
    if hasattr(TestProtocol, attr_name):
        attr_obj = getattr(TestProtocol.__class__, attr_name, None)
        print(f"{attr_name} descriptor: {attr_obj}")
        print(f"  Has __get__: {hasattr(attr_obj, '__get__')}")
        print(f"  Has __set__: {hasattr(attr_obj, '__set__')}")
        print(f"  Has __delete__: {hasattr(attr_obj, '__delete__')}")

print("\n=== Summary ===")
print("This should reveal if PyPy replaces ABC cache attributes during isinstance operations!")