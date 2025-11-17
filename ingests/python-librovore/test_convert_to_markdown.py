#!/usr/bin/env python3

import asyncio
import httpx
from librovore.structures.mkdocs.extraction import parse_mkdocs_html, _convert_to_markdown

async def test_convert_to_markdown():
    """Test the _convert_to_markdown function directly."""
    
    url = "https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel"
    
    # Fetch the actual HTML
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        html_content = response.text
    
    element_id = "pydantic.BaseModel"
    
    print("=== TESTING _convert_to_markdown ===")
    
    # Get the raw description HTML
    parsed_content = parse_mkdocs_html(html_content, element_id, url)
    raw_html = parsed_content['description']
    
    print(f"Raw HTML length: {len(raw_html)}")
    print(f"Raw HTML first 200 chars: {repr(raw_html[:200])}")
    
    # Test the conversion function
    markdown_result = _convert_to_markdown(raw_html)
    
    print(f"\nMarkdown result length: {len(markdown_result)}")
    print(f"Markdown result first 200 chars: {repr(markdown_result[:200])}")
    
    # Check if it's being truncated somehow
    lines = markdown_result.split('\n')
    print(f"Number of lines: {len(lines)}")
    print("First 5 lines:")
    for i, line in enumerate(lines[:5], 1):
        print(f"  {i}: {repr(line)}")

if __name__ == "__main__":
    asyncio.run(test_convert_to_markdown())