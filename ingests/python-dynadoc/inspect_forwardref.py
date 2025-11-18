#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import dynadoc
import inspect
from typing import Annotated

class Provider:
    pass

class Client:
    provider: Annotated['Provider', dynadoc.Doc("Associated service provider")]

# Check what we get
annotations = inspect.get_annotations(Client)
provider_annotation = annotations['provider']

print(f"Full annotation: {provider_annotation!r}")
print(f"Type: {type(provider_annotation)}")
print(f"__args__: {provider_annotation.__args__}")

forwardref = provider_annotation.__args__[0]
print(f"\nForwardRef object: {forwardref!r}")
print(f"ForwardRef type: {type(forwardref)}")
print(f"ForwardRef.__forward_arg__: {getattr(forwardref, '__forward_arg__', 'NOT FOUND')}")

# Check all attributes
print(f"\nForwardRef attributes: {[attr for attr in dir(forwardref) if not attr.startswith('_')]}")
print(f"ForwardRef.__dict__: {getattr(forwardref, '__dict__', {})}")

# Try to get the string
if hasattr(forwardref, '__forward_arg__'):
    print(f"String content: {forwardref.__forward_arg__!r}")
elif hasattr(forwardref, '_name'):
    print(f"String content (via _name): {forwardref._name!r}")
else:
    print("Cannot find string content")