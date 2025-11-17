#!/usr/bin/env python3

import librovore.cli as cli
from librovore import __

print("_filters_default type:", type(cli._filters_default))
print("_filters_default content:", cli._filters_default)
print("_filters_default as dict():", dict(cli._filters_default))
print("is immutable:", hasattr(cli._filters_default, '_data'))

# Check if this might be the issue
try:
    # Simulate what tyro might be doing
    import dataclasses
    import typing

    # Check if the field is seen as having a mutable default
    field_default = cli._filters_default
    print("field_default is empty:", len(field_default) == 0)
    print("field_default is truthy:", bool(field_default))

    # Check what happens when we convert it
    dict_version = dict(field_default)
    print("dict version:", dict_version)
    print("dict version type:", type(dict_version))

except Exception as e:
    print("Error:", e)