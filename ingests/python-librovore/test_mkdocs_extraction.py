#!/usr/bin/env python3
"""
Test script for MkDocs content extraction functionality.
Tests against real sites to validate the implementation.
"""

import asyncio
import json
from pathlib import Path

# Set up the path for librovore imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'sources'))

from librovore.structures.mkdocs import extraction as mkdocs_extraction
from librovore.inventories.sphinx import main as sphinx_inventory
from librovore import interfaces


async def test_mkdocs_extraction():
    """Test MkDocs content extraction with real sites."""
    print("Testing MkDocs content extraction...\n")
    
    # Test sites with known mkdocstrings integration
    test_sites = [
        'https://fastapi.tiangolo.com/',
        'https://docs.pydantic.dev/latest/',
        'https://mkdocstrings.github.io/'
    ]
    
    for site_url in test_sites:
        print(f"Testing {site_url}...")
        
        try:
            # First, get some sample objects from the inventory
            sample_objects = await sphinx_inventory.filter_inventory(
                site_url, 
                filters={'domain': 'py', 'role': 'function'}, 
                details=interfaces.InventoryQueryDetails.Documentation
            )
            
            if not sample_objects:
                print(f"  No inventory objects found for {site_url}")
                continue
                
            print(f"  Found {len(sample_objects)} inventory objects")
            
            # Test extraction with first few objects
            test_objects = sample_objects[:3]
            print(f"  Testing extraction with {len(test_objects)} objects:")
            
            for obj in test_objects:
                print(f"    - {obj['name']} ({obj['role']})")
            
            # Extract content
            extracted_content = await mkdocs_extraction.extract_contents(
                site_url,
                test_objects,
                include_snippets=True
            )
            
            print(f"  Successfully extracted content for {len(extracted_content)} objects")
            
            # Show sample of extracted content
            if extracted_content:
                sample = extracted_content[0]
                print(f"  Sample extraction:")
                print(f"    Object: {sample.get('object_name', 'Unknown')}")
                print(f"    Type: {sample.get('object_type', 'Unknown')}")
                print(f"    URL: {sample.get('url', 'Unknown')}")
                signature = sample.get('signature', '')
                if signature:
                    print(f"    Signature: {signature[:100]}{'...' if len(signature) > 100 else ''}")
                snippet = sample.get('content_snippet', '')
                if snippet:
                    print(f"    Content: {snippet[:150]}{'...' if len(snippet) > 150 else ''}")
            
        except Exception as e:
            print(f"  Error testing {site_url}: {e}")
        
        print()


async def test_theme_detection():
    """Test theme detection and pattern selection."""
    print("Testing theme detection and pattern selection...\n")
    
    test_cases = [
        ('material', 'Material for MkDocs'),
        ('readthedocs', 'ReadTheDocs theme'),
        (None, 'Generic pattern'),
        ('unknown_theme', 'Fallback to generic')
    ]
    
    for theme, description in test_cases:
        print(f"Testing {description}...")
        
        # Test pattern retrieval
        patterns = mkdocs_extraction.MATERIAL_THEME_PATTERNS.get(
            theme, mkdocs_extraction._GENERIC_PATTERN
        )
        
        print(f"  Main content selectors: {len(patterns['main_content_selectors'])}")
        print(f"  API section selectors: {len(patterns['api_section_selectors'])}")
        print(f"  Cleanup selectors: {len(patterns['cleanup_selectors'])}")
        print()


async def main():
    """Main test routine."""
    try:
        await test_theme_detection()
        await test_mkdocs_extraction()
        print("✓ MkDocs extraction testing completed successfully")
        
    except Exception as e:
        print(f"✗ Testing failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    asyncio.run(main())