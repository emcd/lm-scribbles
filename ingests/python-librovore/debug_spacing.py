#!/usr/bin/env python3

import httpx
from bs4 import BeautifulSoup

# Fetch a small sample from tyro docs to debug spacing issues
url = "https://brentyi.github.io/tyro/api/tyro/#tyro.cli"
response = httpx.get(url)
soup = BeautifulSoup(response.text, 'lxml')

# Find the specific element
element = soup.find(id='tyro.cli')
if element:
    print("=== Element found ===")
    print("Element type:", element.name)
    print("Element HTML (first 500 chars):")
    print(str(element)[:500])
    print("\n=== Element text ===")
    print(repr(element.get_text()))
    print("\n=== Children analysis ===")
    for i, child in enumerate(element.children):
        if hasattr(child, 'name') and child.name:
            print(f"Child {i}: <{child.name}> = {repr(child.get_text()[:50])}")
        else:
            print(f"Child {i}: TEXT = {repr(str(child)[:50])}")
else:
    print("Element not found")