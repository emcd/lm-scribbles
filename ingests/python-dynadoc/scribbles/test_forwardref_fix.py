#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import dynadoc
from typing import Annotated

print("=== Testing ForwardRef fix ===")

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
print(Provider.__doc__)
print()
print("Client.__doc__:")
print(Client.__doc__)

# Let's also test by forcing eval_str=True to create ForwardRef objects
print("\n=== Testing with ForwardRef objects directly ===")

import inspect
from typing import ForwardRef

# Monkey patch to force eval_str=True like the doctest environment might
original_access_annotations = dynadoc.introspection._access_annotations

def force_eval_annotations(possessor, context):
    try:
        annotations = dynadoc.introspection.__.inspect.get_annotations(
            possessor, eval_str=True, globals=globals(), locals=locals()
        )
        return dynadoc.introspection.__.types.MappingProxyType(annotations)
    except Exception:
        return original_access_annotations(possessor, context)

dynadoc.introspection._access_annotations = force_eval_annotations

@dynadoc.with_docstring()
class TestClientWithForwardRef:
    ''' Test client with forced ForwardRef. '''
    provider: Annotated['Provider', dynadoc.Doc("Associated service provider")]

print("TestClientWithForwardRef.__doc__:")
print(TestClientWithForwardRef.__doc__)