#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import dynadoc
from typing import ForwardRef

# Test if we can create a scenario where ForwardRef reaches the renderer
original_format_annotation = dynadoc.renderers.sphinxad._format_annotation

def debug_format_annotation(annotation, context, style):
    print(f"_format_annotation received: {annotation!r} (type: {type(annotation)})")
    if isinstance(annotation, ForwardRef):
        print(f"  ForwardRef.__forward_arg__: {annotation.__forward_arg__!r}")
    return original_format_annotation(annotation, context, style)

dynadoc.renderers.sphinxad._format_annotation = debug_format_annotation

# Test direct ForwardRef handling in renderer
ref = ForwardRef('SomeType')
context = dynadoc.produce_context()
result = dynadoc.renderers.sphinxad._format_annotation(ref, context, dynadoc.renderers.sphinxad.Style.Legible)
print(f"Direct ForwardRef result: {result!r}")

# Also test with typing_extensions.ForwardRef
import typing_extensions
ref_ext = typing_extensions.ForwardRef('AnotherType')
result_ext = dynadoc.renderers.sphinxad._format_annotation(ref_ext, context, dynadoc.renderers.sphinxad.Style.Legible)
print(f"typing_extensions.ForwardRef result: {result_ext!r}")