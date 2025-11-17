#!/usr/bin/env python3

# Test the conversion pipeline step by step
import asyncio
import sys
import os

# Add the source directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'sources'))

from librovore.structures.mkdocs.extraction import parse_mkdocs_html, _convert_to_markdown
import httpx

async def debug_conversion():
    # Get the HTML for BaseModel
    url = "https://docs.pydantic.dev/latest/api/base_model/"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        html_content = response.text
    
    # Test our parsing
    try:
        result = parse_mkdocs_html(html_content, "pydantic.BaseModel", url)
        print("=== Raw HTML Description ===")
        print(repr(result['description']))
        
        # Test the conversion
        converted = _convert_to_markdown(result['description'])
        print("\n=== After Markdown Conversion ===")
        print(repr(converted))
        
        # Test if it's the admonition processing
        test_html = '''<div class="admonition abstract">
<p class="admonition-title">Usage Documentation</p>
<p><a href="../../concepts/models/">Models</a></p>
</div>
<p>A base class for creating Pydantic models.</p>'''
        
        print("\n=== Testing Admonition Conversion ===")
        test_converted = _convert_to_markdown(test_html)
        print(repr(test_converted))
        
    except Exception as e:
        print(f"Parsing failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_conversion())