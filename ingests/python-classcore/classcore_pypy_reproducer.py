#!/usr/bin/env python3

"""
Minimal reproducer for PyPy super() issue using only classcore.standard.

This test isolates whether the issue is in classcore itself or in the
more complex inheritance chains involving frigid/appcore.
"""

import sys
print(f"Python implementation: {sys.implementation.name}")
print(f"Python version: {sys.version}")

# Import only classcore.standard components
from classcore.standard.decorators import dataclass_with_standard_behaviors

print("✓ Imported classcore.standard successfully")

# Test 1: Simple dataclass without super() calls
print("\n=== Test 1: Simple dataclass (no methods) ===")
try:
    @dataclass_with_standard_behaviors()
    class SimpleClass:
        name: str = "test"

    obj = SimpleClass()
    print(f"✓ SUCCESS: {obj}")
except Exception as e:
    print(f"✗ FAILED: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Dataclass with method (no super() call)
print("\n=== Test 2: Dataclass with method (no super) ===")
try:
    @dataclass_with_standard_behaviors()
    class ClassWithMethod:
        name: str = "test"

        def get_name(self) -> str:
            return self.name

    obj = ClassWithMethod()
    result = obj.get_name()
    print(f"✓ SUCCESS: {result}")
except Exception as e:
    print(f"✗ FAILED: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Dataclass with inheritance (no super() call)
print("\n=== Test 3: Dataclass with inheritance (no super) ===")
try:
    @dataclass_with_standard_behaviors()
    class BaseClass:
        base_value: int = 42

        def get_base(self) -> int:
            return self.base_value

    @dataclass_with_standard_behaviors()
    class DerivedClass(BaseClass):
        derived_value: str = "derived"

        def get_derived(self) -> str:
            return self.derived_value

    obj = DerivedClass()
    print(f"✓ SUCCESS: base={obj.get_base()}, derived={obj.get_derived()}")
except Exception as e:
    print(f"✗ FAILED: {e}")
    import traceback
    traceback.print_exc()

# Test 4: The critical test - method with super() call
print("\n=== Test 4: CRITICAL - Method with super() call ===")
try:
    @dataclass_with_standard_behaviors()
    class BaseWithInit:
        base_value: int = 42

        def initialize(self) -> str:
            return f"base: {self.base_value}"

    @dataclass_with_standard_behaviors()
    class DerivedWithSuper(BaseWithInit):
        derived_value: str = "derived"

        def initialize(self) -> str:
            # This should trigger the PyPy issue if it exists in classcore
            base_result = super().initialize()
            return f"{base_result}, derived: {self.derived_value}"

    obj = DerivedWithSuper()
    result = obj.initialize()
    print(f"✓ SUCCESS: {result}")
except Exception as e:
    print(f"✗ FAILED: {e}")
    import traceback
    traceback.print_exc()

# Test 5: More complex inheritance with super()
print("\n=== Test 5: Complex inheritance with super() ===")
try:
    @dataclass_with_standard_behaviors()
    class GrandParent:
        grand_value: str = "grand"

        def process(self) -> str:
            return f"grand({self.grand_value})"

    @dataclass_with_standard_behaviors()
    class Parent(GrandParent):
        parent_value: int = 100

        def process(self) -> str:
            grand_result = super().process()
            return f"parent({self.parent_value}) -> {grand_result}"

    @dataclass_with_standard_behaviors()
    class Child(Parent):
        child_value: float = 3.14

        def process(self) -> str:
            parent_result = super().process()
            return f"child({self.child_value}) -> {parent_result}"

    obj = Child()
    result = obj.process()
    print(f"✓ SUCCESS: {result}")
except Exception as e:
    print(f"✗ FAILED: {e}")
    import traceback
    traceback.print_exc()

# Test 6: Async method with super() (similar to the appcore issue)
print("\n=== Test 6: Async method with super() ===")
try:
    @dataclass_with_standard_behaviors()
    class AsyncBase:
        async_value: str = "async_base"

        async def prepare(self) -> str:
            return f"prepared: {self.async_value}"

    @dataclass_with_standard_behaviors()
    class AsyncDerived(AsyncBase):
        derived_async_value: str = "async_derived"

        async def prepare(self) -> str:
            # This mimics the appcore pattern that fails in PyPy
            base_result = await super().prepare()
            return f"{base_result} + {self.derived_async_value}"

    obj = AsyncDerived()
    # We can't easily test async here, but class creation is what matters
    print(f"✓ SUCCESS: Async class created: {obj}")
except Exception as e:
    print(f"✗ FAILED: {e}")
    import traceback
    traceback.print_exc()

print(f"\n=== Summary for {sys.implementation.name} ===")
print("If Test 4, 5, or 6 failed in PyPy but passed in CPython,")
print("then we've reproduced the issue in pure classcore.standard.")