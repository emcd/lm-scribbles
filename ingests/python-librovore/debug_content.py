#!/usr/bin/env python3

import json

# Test the actual content from the JSON output
description_from_json = """Return a new dictionary initialized from an optional positional argument
and a possibly empty set of keyword arguments.
Dictionaries can be created by several means:
Use a comma-separated list of key: value pairs within braces:
{'jack': 4098, 'sjoerd': 4127} or {4098: 'jack', 4127: 'sjoerd'}
Use a dict comprehension: {}, {x: x ** 2 for x in range(10)}
Use the type constructor: dict(),
dict([('foo', 100), ('bar', 200)]), dict(foo=100, bar=200)"""

print("Description content preview:")
print(repr(description_from_json[:200]))
print()
print("Description content rendered:")
print(description_from_json[:200])
print()

# This content looks like plain text, not HTML
# Let's check if it's being passed through html_to_markdown inappropriately
from librovore.structures.sphinx.conversion import html_to_markdown

result = html_to_markdown(description_from_json)
print("After html_to_markdown:")
print(repr(result[:100]))
print()
print("Rendered:")
print(result[:200])