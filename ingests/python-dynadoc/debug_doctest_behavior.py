#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Debug script to understand the doctest Advanced context behavior.
"""

# Set up the exact same imports as the doctest
import dynadoc
import dynadoc.xtnsapi as xtnsapi
from typing import Annotated

print("=== Initial setup complete ===")

# Now add the future import (this should be at module level)
exec("from __future__ import annotations")

print("=== Future annotations imported ===")

# Create the classes exactly as in the doctest
code = '''
@dynadoc.with_docstring()
class Provider:
    """ Service provider that manages clients. """
    
    name: Annotated[str, dynadoc.Doc("Provider service name")]
    
    def create_client(self, config: dict) -> 'Client':
        """ Creates a new client instance. """
        return Client(provider=self, name=config.get('name', 'default'))

@dynadoc.with_docstring()
class Client:
    """ Service client that connects to a provider. """
    
    provider: Annotated['Provider', dynadoc.Doc("Associated service provider")]
    name: Annotated[str, dynadoc.Doc("Client instance name")]
    
    def get_provider_info(self) -> 'Provider':
        """ Returns information about the associated provider. """
        return self.provider
'''

# Execute in current namespace
exec(code)

print("=== Classes created ===")

print("\nProvider.__doc__:")
print(repr(Provider.__doc__))

print("\nClient.__doc__:")
print(repr(Client.__doc__))

# Check annotations
import inspect
print("\nAnnotations check:")
annotations = inspect.get_annotations(Client)
for name, annotation in annotations.items():
    print(f"  {name}: {annotation!r} (type: {type(annotation)})")

# Let's also try to see what happens in the dynadoc internals
print("\n=== Debugging dynadoc internals ===")

# Let's monkey patch to see what's happening
original_access_annotations = dynadoc.introspection._access_annotations

def debug_access_annotations(possessor, context):
    print(f"_access_annotations called on {possessor}")
    result = original_access_annotations(possessor, context)
    print(f"_access_annotations returned: {dict(result)}")
    for name, annotation in result.items():
        print(f"  {name}: {annotation!r} (type: {type(annotation)})")
    return result

dynadoc.introspection._access_annotations = debug_access_annotations

print("\n=== Creating classes with debug enabled ===")

@dynadoc.with_docstring()
class DebugClient:
    """ Debug client class. """
    provider: Annotated['Provider', dynadoc.Doc("Associated service provider")]

print("\nDebugClient.__doc__:")
print(repr(DebugClient.__doc__))