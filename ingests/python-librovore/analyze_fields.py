#!/usr/bin/env python3

# Based on the JSON output, let me analyze the two fields:

description = """Return a new dictionary initialized from an optional positional argument
and a possibly empty set of keyword arguments.
Dictionaries can be created by several means:
Use a comma-separated list of key: value pairs within braces:
{'jack': 4098, 'sjoerd': 4127} or {4098: 'jack', 4127: 'sjoerd'}
Use a dict comprehension: {}, {x: x ** 2 for x in range(10)}
Use the type constructor: dict(),
dict([('foo', 100), ('bar', 200)]), dict(foo=100, bar=200)
[... continues for ~8000 characters with full documentation]"""

content_snippet = """Return a new dictionary initialized from an optional positional argument
and a possibly empty set of keyword arguments.
Dictionaries can be created by several means:
Use a comma-separated list of key:..."""

print("Description length:", len(description))
print("Content snippet length:", len(content_snippet))
print()
print("Description preview (first 200 chars):")
print(repr(description[:200]))
print()
print("Content snippet (full):")
print(repr(content_snippet))
print()
print("Are they the same content?", content_snippet.startswith(description[:len(content_snippet)-3]))