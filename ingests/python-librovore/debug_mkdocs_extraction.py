#!/usr/bin/env python3

# Test the MkDocs extraction pipeline directly
import asyncio
import sys
import os

# Add the source directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'sources'))

from librovore.structures.mkdocs.extraction import parse_mkdocs_html
import httpx

async def test_extraction():
    # Get the HTML for BaseModel
    url = "https://docs.pydantic.dev/latest/api/base_model/"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        html_content = response.text
    
    # Test our parsing
    try:
        result = parse_mkdocs_html(html_content, "pydantic.BaseModel", url)
        print("=== Parsing Result ===")
        print(f"Signature: {repr(result['signature'])}")
        print(f"Description (raw HTML): {repr(result['description'])}")
        print(f"Object name: {repr(result['object_name'])}")
        
        # Test the conversion separately
        from librovore.structures.mkdocs.extraction import _convert_to_markdown
        converted = _convert_to_markdown(result['description'])
        print(f"After conversion: {repr(converted)}")
        
    except Exception as e:
        print(f"Parsing failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_extraction())