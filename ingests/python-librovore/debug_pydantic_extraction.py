#!/usr/bin/env python3

import asyncio
from bs4 import BeautifulSoup
import httpx

async def debug_pydantic_extraction():
    """Debug the Pydantic BaseModel content extraction."""
    
    url = "https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel"
    
    # Fetch the actual HTML
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        html_content = response.text
    
    print("=== HTML STRUCTURE ANALYSIS ===")
    soup = BeautifulSoup(html_content, 'lxml')
    
    # Look for the target element
    target = soup.find(id='pydantic.BaseModel')
    print(f"Element with id='pydantic.BaseModel': {target is not None}")
    
    if target:
        print(f"Target element tag: {target.name}")
        print(f"Target element classes: {target.get('class', [])}")
        print(f"Target element content preview: {str(target)[:200]}...")
    
    # Look for doc-contents containers
    doc_contents = soup.find_all(class_='doc-contents')
    print(f"\nFound {len(doc_contents)} .doc-contents elements")
    
    # Look for main content containers
    main_containers = [
        soup.find('article', role='main'),
        soup.find(class_='md-content__inner'),
        soup.find(class_='md-typeset'),
        soup.find('main', class_='md-content'),
    ]
    
    print("\nMain content containers:")
    for i, container in enumerate(main_containers):
        print(f"{i+1}. {container is not None} - {container.name if container else 'None'}")
    
    # If target found, simulate MkDocs extraction
    if target:
        print("\n=== SIMULATING MKDOCS EXTRACTION ===")
        from librovore.structures.mkdocs.extraction import _find_doc_contents_container
        
        doc_contents_container = _find_doc_contents_container(target)
        print(f"Found doc-contents container: {doc_contents_container is not None}")
        
        if doc_contents_container:
            inner_html = doc_contents_container.decode_contents()
            print(f"Inner HTML length: {len(inner_html)}")
            print(f"Inner HTML preview: {inner_html[:300]}...")
        else:
            print("No doc-contents found, checking fallback content...")
            print(f"Target element content: {str(target)[:300]}...")

if __name__ == "__main__":
    asyncio.run(debug_pydantic_extraction())