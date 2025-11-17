#!/usr/bin/env python3

import httpx
from bs4 import BeautifulSoup
import asyncio

async def examine_structure():
    url = "https://docs.pydantic.dev/latest/api/base_model/"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        html = response.text
    
    soup = BeautifulSoup(html, 'lxml')
    
    # Find the main content container
    main_container = soup.select_one('article[role="main"]')
    if not main_container:
        main_container = soup.select_one('.md-content__inner')
    
    print("=== Main container found ===")
    
    # Find the BaseModel element
    target_element = main_container.find(id='pydantic.BaseModel')
    print(f"Target element found: {target_element is not None}")
    
    if target_element:
        print("\n=== Target element structure ===")
        print("Tag:", target_element.name)
        print("Classes:", target_element.get('class', []))
        print("ID:", target_element.get('id'))
        
        # Look at the parent structure
        parent = target_element.parent
        print(f"\nParent: {parent.name if parent else None}, classes: {parent.get('class', []) if parent else []}")
        
        # Look at all siblings to understand the structure
        print("\n=== All siblings after target ===")
        sibling = target_element.next_sibling
        sibling_count = 0
        while sibling and sibling_count < 5:  # Limit to avoid too much output
            if hasattr(sibling, 'name') and sibling.name:
                print(f"Sibling {sibling_count}: {sibling.name}, classes: {sibling.get('class', [])}")
                # Check if this is the right doc-contents
                if 'doc-contents' in sibling.get('class', []):
                    print("  This is a doc-contents!")
                    # Check if it has the 'first' class which might indicate main content
                    if 'first' in sibling.get('class', []):
                        print("  And it has 'first' class!")
                        # Show first few children
                        for i, child in enumerate(sibling.children):
                            if i >= 3:  # Limit output
                                break
                            if hasattr(child, 'name') and child.name:
                                print(f"    Child {i}: {child.name}, classes: {child.get('class', [])}")
                                if child.name == 'p':
                                    text = child.get_text().strip()
                                    print(f"      Text: {repr(text[:80])}")
                                elif child.name == 'div' and 'admonition' in child.get('class', []):
                                    admon_type = [c for c in child.get('class', []) if c != 'admonition']
                                    print(f"      Admonition type: {admon_type}")
                                    title_elem = child.select_one('.admonition-title')
                                    if title_elem:
                                        print(f"      Title: {repr(title_elem.get_text().strip())}")
            sibling = sibling.next_sibling
            sibling_count += 1

if __name__ == "__main__":
    asyncio.run(examine_structure())