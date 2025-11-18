#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import sys
import inspect
from typing import ForwardRef

print(f"Python version: {sys.version}")
print(f"Python version info: {sys.version_info}")

# Test ForwardRef attributes
print("\n=== Testing ForwardRef object ===")

# Create a ForwardRef directly
ref = ForwardRef('SomeType')
print(f"ForwardRef object: {ref!r}")
print(f"ForwardRef type: {type(ref)}")

# Check for __forward_arg__
if hasattr(ref, '__forward_arg__'):
    print(f"__forward_arg__: {ref.__forward_arg__!r}")
else:
    print("__forward_arg__ NOT FOUND")

# Check for alternative attributes
alt_attrs = ['_name', '__forward_value__', 'arg']
for attr in alt_attrs:
    if hasattr(ref, attr):
        print(f"{attr}: {getattr(ref, attr)!r}")

# Show all public attributes
print(f"All attributes: {[attr for attr in dir(ref) if not attr.startswith('_')]}")

# Test with typing_extensions if available
print("\n=== Testing typing_extensions ===")
try:
    import typing_extensions as typx
    print(f"typing_extensions version: {getattr(typx, '__version__', 'unknown')}")
    
    # Test if it has get_annotations
    if hasattr(typx, 'get_annotations'):
        print("typing_extensions.get_annotations is available")
        
        # Create test class
        class TestClass:
            field: 'SomeType'
        
        # Compare behaviors
        print("\n--- inspect.get_annotations ---")
        std_annotations = inspect.get_annotations(TestClass)
        for name, annotation in std_annotations.items():
            print(f"  {name}: {annotation!r} (type: {type(annotation)})")
        
        print("\n--- typing_extensions.get_annotations ---")
        ext_annotations = typx.get_annotations(TestClass)
        for name, annotation in ext_annotations.items():
            print(f"  {name}: {annotation!r} (type: {type(annotation)})")
        
        print("\n--- typing_extensions.get_annotations with eval_str=True ---")
        try:
            ext_annotations_eval = typx.get_annotations(TestClass, eval_str=True, globals=globals(), locals=locals())
            for name, annotation in ext_annotations_eval.items():
                print(f"  {name}: {annotation!r} (type: {type(annotation)})")
                if hasattr(annotation, '__forward_arg__'):
                    print(f"    __forward_arg__: {annotation.__forward_arg__!r}")
        except Exception as e:
            print(f"  Error: {e}")
    else:
        print("typing_extensions.get_annotations is NOT available")
        
except ImportError:
    print("typing_extensions not available")

# Test ForwardRef in annotation context
print("\n=== Testing ForwardRef in Annotated context ===")
from typing import Annotated
import dynadoc

class TestAnnotated:
    field: Annotated['SomeType', dynadoc.Doc("Test field")]

# Get with eval_str=True to force ForwardRef creation
try:
    eval_annotations = inspect.get_annotations(TestAnnotated, eval_str=True, globals=globals(), locals=locals())
    for name, annotation in eval_annotations.items():
        print(f"{name}: {annotation!r}")
        if hasattr(annotation, '__args__'):
            for i, arg in enumerate(annotation.__args__):
                print(f"  arg[{i}]: {arg!r} (type: {type(arg)})")
                if hasattr(arg, '__forward_arg__'):
                    print(f"    __forward_arg__: {arg.__forward_arg__!r}")
                elif hasattr(arg, '_name'):
                    print(f"    _name: {arg._name!r}")
except Exception as e:
    print(f"Error getting evaluated annotations: {e}")