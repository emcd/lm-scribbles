#!/usr/bin/env python3

import asyncio
import httpx
from librovore.structures.mkdocs.extraction import parse_mkdocs_html, _convert_to_markdown

async def test_full_extraction_path():
    """Test the full extraction path step by step."""
    
    url = "https://docs.pydantic.dev/latest/api/base_model/#pydantic.BaseModel"
    
    # Fetch the actual HTML
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        html_content = response.text
    
    element_id = "pydantic.BaseModel"
    
    print("=== STEP-BY-STEP EXTRACTION TEST ===")
    
    # Step 1: Parse HTML
    print("1. Parsing HTML...")
    try:
        parsed_content = parse_mkdocs_html(html_content, element_id, url)
        print(f"   ✓ Success. Description length: {len(parsed_content['description'])}")
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        return
    
    # Step 2: Convert to markdown
    print("2. Converting to markdown...")
    try:
        description = _convert_to_markdown(parsed_content['description'])
        print(f"   ✓ Success. Markdown length: {len(description)}")
        lines = description.split('\n')
        print(f"   First line: {repr(lines[0])}")
        print(f"   Line count: {len(lines)}")
    except Exception as e:
        print(f"   ✗ Failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Step 3: Create snippet
    print("3. Creating snippet...")
    snippet_max_length = 200
    if len(description) > snippet_max_length:
        content_snippet = description[:snippet_max_length] + '...'
    else:
        content_snippet = description
    print(f"   ✓ Snippet length: {len(content_snippet)}")
    print(f"   Snippet: {repr(content_snippet)}")
    
    # Step 4: Final result structure
    print("4. Final result structure...")
    result = {
        'description': description,
        'content_snippet': content_snippet,
    }
    
    print(f"   Description length: {len(result['description'])}")
    print(f"   Snippet length: {len(result['content_snippet'])}")
    print(f"   Description == Snippet: {result['description'] == result['content_snippet']}")

if __name__ == "__main__":
    asyncio.run(test_full_extraction_path())