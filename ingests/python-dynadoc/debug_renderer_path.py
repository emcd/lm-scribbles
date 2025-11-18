#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import dynadoc
from typing import Annotated

# Monkey patch the renderer to see what annotations it receives
original_format_annotation = dynadoc.renderers.sphinxad._format_annotation

def debug_format_annotation(annotation, context, style):
    print(f"_format_annotation received: {annotation!r} (type: {type(annotation)})")
    return original_format_annotation(annotation, context, style)

dynadoc.renderers.sphinxad._format_annotation = debug_format_annotation

@dynadoc.with_docstring()
class TestClass:
    ''' Test class to see what annotations reach the renderer. '''
    provider: Annotated['Provider', dynadoc.Doc("Associated service provider")]
    name: Annotated[str, dynadoc.Doc("Client instance name")]

print("TestClass.__doc__:")
print(TestClass.__doc__)