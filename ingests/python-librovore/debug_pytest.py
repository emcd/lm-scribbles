#!/usr/bin/env python3

import httpx
from bs4 import BeautifulSoup

# Debug pytest fixture extraction
url = "https://docs.pytest.org/en/latest/reference/fixtures.html#fixture"
response = httpx.get(url)
soup = BeautifulSoup(response.text, 'lxml')

# Find the main content container like our code does (Furo theme)
containers = [
    soup.find('article', {'role': 'main'}),
    soup.find('div', {'id': 'furo-main-content'}),
]

container = None
for c in containers:
    if c:
        container = c
        break

if container:
    print("=== Container found ===")
    element = container.find(id='fixture')
    if element:
        print(f"=== Element found: {element.name} ===")
        print("Element HTML (first 500 chars):")
        print(str(element)[:500])
        print("\n=== Element text ===")
        print(repr(element.get_text()[:200]))
        
        print("\n=== Next sibling analysis ===")
        next_sib = element.find_next_sibling()
        if next_sib:
            print(f"Next sibling: {next_sib.name}")
            print(f"Next sibling text: {repr(next_sib.get_text()[:200])}")
        else:
            print("No next sibling found")
            
        print("\n=== Parent analysis ===")
        if element.parent:
            print(f"Parent: {element.parent.name}")
            parent_next = element.parent.find_next_sibling()
            if parent_next:
                print(f"Parent next sibling: {parent_next.name}")
                print(f"Parent next text: {repr(parent_next.get_text()[:200])}")
            else:
                print("No parent next sibling")
                
        print("\n=== Looking for p elements ===")
        # Check different strategies
        next_p = element.find_next('p')
        if next_p:
            print(f"Next p element: {repr(next_p.get_text()[:200])}")
        else:
            print("No next p found")
            
    else:
        print("Element 'fixture' not found in container")
else:
    print("Container not found")