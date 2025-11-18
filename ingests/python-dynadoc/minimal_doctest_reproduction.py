#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Minimal reproduction of the exact doctest code to see what's happening.
"""

from __future__ import annotations

import dynadoc
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
print()
print("Client.__doc__:")
print(repr(Client.__doc__))
print()

# Let's also check what inspect.get_annotations returns here
import inspect
print("inspect.get_annotations(Client):")
annotations = inspect.get_annotations(Client)
for name, annotation in annotations.items():
    print(f"  {name}: {annotation!r} (type: {type(annotation)})")