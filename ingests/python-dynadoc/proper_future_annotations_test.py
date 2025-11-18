#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This should be the VERY first line (like in the doctest)
from __future__ import annotations

import dynadoc
import dynadoc.xtnsapi as xtnsapi
from typing import Annotated

@dynadoc.with_docstring()
class Provider:
    ''' Service provider that manages clients. '''
    
    name: Annotated[str, dynadoc.Doc("Provider service name")]
    
    def create_client(self, config: dict) -> 'Client':
        ''' Creates a new client instance. '''
        return Client(provider=self, name=config.get('name', 'default'))

@dynadoc.with_docstring()
class Client:
    ''' Service client that connects to a provider. '''
    
    provider: Annotated['Provider', dynadoc.Doc("Associated service provider")]
    name: Annotated[str, dynadoc.Doc("Client instance name")]
    
    def get_provider_info(self) -> 'Provider':
        ''' Returns information about the associated provider. '''
        return self.provider

print("Provider.__doc__:")
print(repr(Provider.__doc__))

print("\nClient.__doc__:")
print(repr(Client.__doc__))

# Check annotations
import inspect
print("\nAnnotations:")
annotations = inspect.get_annotations(Client)
for name, annotation in annotations.items():
    print(f"  {name}: {annotation!r} (type: {type(annotation)})")

# Also check with eval_str=True
print("\nAnnotations with eval_str=True:")
try:
    annotations_eval = inspect.get_annotations(Client, eval_str=True, globals=globals(), locals=locals())
    for name, annotation in annotations_eval.items():
        print(f"  {name}: {annotation!r} (type: {type(annotation)})")
        if hasattr(annotation, '__args__'):
            for i, arg in enumerate(annotation.__args__):
                print(f"    arg[{i}]: {arg!r} (type: {type(arg)})")
                if hasattr(arg, '__forward_arg__'):
                    print(f"      __forward_arg__: {arg.__forward_arg__!r}")
except Exception as e:
    print(f"Error: {e}")