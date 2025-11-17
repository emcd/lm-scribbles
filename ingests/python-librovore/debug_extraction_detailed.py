#!/usr/bin/env python3

# Debug the exact extraction flow
import asyncio
import sys
import os

# Add the source directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'sources'))

from librovore.structures.mkdocs.extraction import (
    parse_mkdocs_html, _find_doc_contents_container, 
    _extract_paragraphs_from_doc_contents, _extract_using_fallback_selectors,
    MATERIAL_THEME_PATTERNS, _GENERIC_PATTERN
)
from bs4 import BeautifulSoup
import httpx

async def debug_detailed_extraction():
    # Get the HTML for BaseModel
    url = "https://docs.pydantic.dev/latest/api/base_model/"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        html_content = response.text
    
    print("=== Full Extraction Debug ===")
    
    # Parse HTML and find elements like our code does
    soup = BeautifulSoup(html_content, 'lxml')
    main_container = soup.select_one('article[role="main"]')
    if not main_container:
        main_container = soup.select_one('.md-content__inner')
    
    target_element = main_container.find(id='pydantic.BaseModel')
    print(f"Target element: {target_element.name if target_element else None}")
    
    if target_element:
        # Test our doc-contents finding
        doc_contents = _find_doc_contents_container(target_element)
        print(f"Doc contents found: {doc_contents is not None}")
        
        if doc_contents:
            # Test paragraph extraction
            descriptions = _extract_paragraphs_from_doc_contents(doc_contents)
            print(f"Paragraphs extracted: {descriptions}")
        else:
            print("No doc-contents found, testing fallback...")
            # Test fallback selectors
            patterns = MATERIAL_THEME_PATTERNS.get('material', _GENERIC_PATTERN)
            descriptions = _extract_using_fallback_selectors(target_element, patterns)
            print(f"Fallback descriptions: {descriptions}")
    
    # Also test the full parse function
    print("\n=== Full Parse Function ===")
    try:
        result = parse_mkdocs_html(html_content, "pydantic.BaseModel", url)
        print(f"Full parse result: {repr(result['description'])}")
    except Exception as e:
        print(f"Full parse failed: {e}")

if __name__ == "__main__":
    asyncio.run(debug_detailed_extraction())