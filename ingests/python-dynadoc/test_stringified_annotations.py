#!/usr/bin/env python3
# vim: set filetype=python fileencoding=utf-8:
# -*- coding: utf-8 -*-

"""
Test script to understand how stringified annotations are handled
and what objects we actually get from inspect.get_annotations.
"""

from __future__ import annotations

import inspect
import sys
from typing import Annotated

# Import dynadoc to test current behavior
import dynadoc


print(f"Python version: {sys.version}")
print(f"Python version info: {sys.version_info}")
print()


class Provider:
    """Service provider that manages clients."""
    
    name: Annotated[str, dynadoc.Doc("Provider service name")]
    
    def create_client(self, config: dict) -> Client:
        """Creates a new client instance."""
        return Client(provider=self, name=config.get('name', 'default'))


class Client:
    """Service client that connects to a provider."""
    
    provider: Annotated[Provider, dynadoc.Doc("Associated service provider")]
    name: Annotated[str, dynadoc.Doc("Client instance name")]
    
    def get_provider_info(self) -> Provider:
        """Returns information about the associated provider."""
        return self.provider


# Test what inspect.get_annotations returns
print("=== Testing inspect.get_annotations behavior ===")

print("\n--- Client annotations (default) ---")
client_annotations = inspect.get_annotations(Client)
for name, annotation in client_annotations.items():
    print(f"{name}: {annotation!r}")
    print(f"  type: {type(annotation)}")
    if hasattr(annotation, '__forward_arg__'):
        print(f"  __forward_arg__: {annotation.__forward_arg__!r}")
    if hasattr(annotation, '__args__'):
        print(f"  __args__: {annotation.__args__}")
        for i, arg in enumerate(annotation.__args__):
            print(f"    arg[{i}]: {arg!r} (type: {type(arg)})")
            if hasattr(arg, '__forward_arg__'):
                print(f"      __forward_arg__: {arg.__forward_arg__!r}")
    print()

print("\n--- Client annotations (eval_str=False) ---")
try:
    client_annotations_no_eval = inspect.get_annotations(Client, eval_str=False)
    for name, annotation in client_annotations_no_eval.items():
        print(f"{name}: {annotation!r}")
        print(f"  type: {type(annotation)}")
        if hasattr(annotation, '__forward_arg__'):
            print(f"  __forward_arg__: {annotation.__forward_arg__!r}")
        if hasattr(annotation, '__args__'):
            print(f"  __args__: {annotation.__args__}")
            for i, arg in enumerate(annotation.__args__):
                print(f"    arg[{i}]: {arg!r} (type: {type(arg)})")
                if hasattr(arg, '__forward_arg__'):
                    print(f"      __forward_arg__: {arg.__forward_arg__!r}")
        print()
except Exception as e:
    print(f"Error with eval_str=False: {e}")

print("\n--- Client annotations (eval_str=True with globals/locals) ---")
try:
    client_annotations_eval = inspect.get_annotations(
        Client, 
        eval_str=True, 
        globals=globals(), 
        locals=locals()
    )
    for name, annotation in client_annotations_eval.items():
        print(f"{name}: {annotation!r}")
        print(f"  type: {type(annotation)}")
        if hasattr(annotation, '__forward_arg__'):
            print(f"  __forward_arg__: {annotation.__forward_arg__!r}")
        if hasattr(annotation, '__args__'):
            print(f"  __args__: {annotation.__args__}")
            for i, arg in enumerate(annotation.__args__):
                print(f"    arg[{i}]: {arg!r} (type: {type(arg)})")
                if hasattr(arg, '__forward_arg__'):
                    print(f"      __forward_arg__: {arg.__forward_arg__!r}")
        print()
except Exception as e:
    print(f"Error with eval_str=True: {e}")

print("\n--- Provider annotations ---")
provider_annotations = inspect.get_annotations(Provider)
for name, annotation in provider_annotations.items():
    print(f"{name}: {annotation!r}")
    print(f"  type: {type(annotation)}")
    if hasattr(annotation, '__forward_arg__'):
        print(f"  __forward_arg__: {annotation.__forward_arg__!r}")
    if hasattr(annotation, '__args__'):
        print(f"  __args__: {annotation.__args__}")
        for i, arg in enumerate(annotation.__args__):
            print(f"    arg[{i}]: {arg!r} (type: {type(arg)})")
            if hasattr(arg, '__forward_arg__'):
                print(f"      __forward_arg__: {arg.__forward_arg__!r}")
    print()


# Test dynadoc's current behavior
print("\n=== Testing dynadoc's current behavior ===")

@dynadoc.with_docstring()
class TestProvider:
    """Service provider that manages clients."""
    
    name: Annotated[str, dynadoc.Doc("Provider service name")]


@dynadoc.with_docstring()
class TestClient:
    """Service client that connects to a provider."""
    
    provider: Annotated[TestProvider, dynadoc.Doc("Associated service provider")]
    name: Annotated[str, dynadoc.Doc("Client instance name")]


print("\nTestProvider.__doc__:")
print(repr(TestProvider.__doc__))

print("\nTestClient.__doc__:")
print(repr(TestClient.__doc__))