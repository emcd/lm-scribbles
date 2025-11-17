#!/usr/bin/env python3

from bs4 import BeautifulSoup
import urllib.request

# Get the HTML
response = urllib.request.urlopen('https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel')
html = response.read().decode('utf-8')
soup = BeautifulSoup(html, 'lxml')

# Find the main content container
main_container = soup.select_one('article[role="main"]')
if not main_container:
    main_container = soup.select_one('.md-content__inner')

# Find the BaseModel element
target_element = main_container.find(id='pydantic.BaseModel')
print('Target element found:', target_element is not None)

if target_element:
    # Extract using our current description selectors
    desc_selectors = ['.doc-contents', '.doc-object-member .doc-contents', 'p', '.admonition']
    for selector in desc_selectors:
        elements = target_element.select(selector)
        print(f'Selector {selector}: {len(elements)} elements')
        for i, elem in enumerate(elements[:3]):  # Show first 3
            text = elem.get_text().strip()
            print(f'  {i}: {text[:100]}...')
        print()
    
    # Try to find the actual description paragraph
    print("=== Looking for the main description ===")
    
    # Look for the paragraph right after the admonition
    doc_contents = target_element.select_one('.doc-contents')
    if doc_contents:
        # Look for p elements that are direct children or immediate siblings
        p_elements = doc_contents.select('p')
        print(f"Found {len(p_elements)} p elements in doc-contents")
        for i, p in enumerate(p_elements):
            text = p.get_text().strip()
            if text and not text.startswith('Usage Documentation'):
                print(f"  P{i}: {text}")
    
    # Alternative: look for the first p element after the admonition
    admonition = target_element.select_one('.admonition')
    if admonition:
        print("Found admonition, looking for next siblings...")
        next_elem = admonition.next_sibling
        while next_elem:
            if hasattr(next_elem, 'name') and next_elem.name == 'p':
                text = next_elem.get_text().strip()
                if text:
                    print(f"  Next p after admonition: {text}")
                    break
            next_elem = next_elem.next_sibling