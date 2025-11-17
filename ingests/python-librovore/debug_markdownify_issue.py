#!/usr/bin/env python3

import asyncio
import markdownify
from bs4 import BeautifulSoup
import httpx

async def debug_markdownify_issue():
    """Debug why markdownify is returning just 'Usage Documentation'."""
    
    url = "https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel"
    
    # Fetch the actual HTML
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        html_content = response.text
    
    soup = BeautifulSoup(html_content, 'lxml')
    target = soup.find(id='pydantic.BaseModel')
    
    if target:
        # Find doc-contents
        from librovore.structures.mkdocs.extraction import _find_doc_contents_container
        doc_contents_container = _find_doc_contents_container(target)
        
        if doc_contents_container:
            inner_html = doc_contents_container.decode_contents()
            
            print("=== FIRST 1000 CHARS OF INNER HTML ===")
            print(inner_html[:1000])
            
            print("\n=== MARKDOWNIFY RESULT ===")
            markdown_result = markdownify.markdownify(inner_html, heading_style='ATX')
            print(f"Markdown length: {len(markdown_result)}")
            print("First 500 chars:")
            print(repr(markdown_result[:500]))
            
            print("\nFirst 10 lines:")
            lines = markdown_result.split('\n')
            for i, line in enumerate(lines[:10]):
                print(f"{i+1}: {repr(line)}")

if __name__ == "__main__":
    asyncio.run(debug_markdownify_issue())