#!/usr/bin/env python3

import asyncio
import httpx
from librovore.structures.mkdocs.extraction import parse_mkdocs_html
import markdownify

async def debug_parse_mkdocs():
    """Debug the parse_mkdocs_html function specifically."""
    
    url = "https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel"
    
    # Fetch the actual HTML
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        html_content = response.text
    
    element_id = "pydantic.BaseModel"
    
    print("=== TESTING parse_mkdocs_html ===")
    
    try:
        parsed_content = parse_mkdocs_html(html_content, element_id, url)
        
        print(f"Parsed content keys: {list(parsed_content.keys())}")
        
        for key, value in parsed_content.items():
            print(f"\n{key}:")
            print(f"  Type: {type(value)}")
            print(f"  Length: {len(str(value))}")
            if key == 'description':
                print(f"  First 500 chars: {repr(str(value)[:500])}")
                # Test markdownify on this
                markdown_result = markdownify.markdownify(str(value), heading_style='ATX')
                print(f"  Markdownify result length: {len(markdown_result)}")
                print(f"  Markdownify first 200 chars: {repr(markdown_result[:200])}")
            else:
                print(f"  Value: {repr(str(value))}")
                
    except Exception as e:
        print(f"Error in parse_mkdocs_html: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_parse_mkdocs())