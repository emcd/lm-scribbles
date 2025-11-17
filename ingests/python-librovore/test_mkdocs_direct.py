#!/usr/bin/env python3
"""
Direct test of MkDocs processor functionality without MCP registration.
"""

import asyncio
from pathlib import Path

# Set up the path for librovore imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'sources'))

from librovore.structures.mkdocs.main import MkDocsProcessor
from librovore.inventories.sphinx import main as sphinx_inventory
from librovore import interfaces


async def test_mkdocs_processor_direct():
    """Test MkDocs processor directly without MCP registration."""
    print("Testing MkDocs processor directly...\n")
    
    # Test site
    test_url = 'https://fastapi.tiangolo.com/'
    
    print(f"Testing with {test_url}")
    
    try:
        # Step 1: Create MkDocs processor
        processor = MkDocsProcessor()
        print(f"1. Created MkDocs processor: {processor.name}")
        
        # Step 2: Test detection
        print("\n2. Testing detection...")
        detection = await processor.detect(test_url)
        print(f"   Confidence: {detection.confidence}")
        print(f"   Theme: {getattr(detection, 'theme', 'Unknown')}")
        print(f"   Has mkdocs.yml: {getattr(detection, 'has_mkdocs_yml', 'Unknown')}")
        
        # Step 3: Get inventory objects
        print("\n3. Getting inventory objects...")
        sample_objects = await sphinx_inventory.filter_inventory(
            test_url, 
            filters={'domain': 'py', 'role': 'class'}, 
            details=interfaces.InventoryQueryDetails.Documentation
        )
        
        print(f"   Found {len(sample_objects)} inventory objects")
        
        if sample_objects:
            # Step 4: Test content extraction
            print("\n4. Testing content extraction...")
            test_objects = sample_objects[:2]  # Test with first 2 objects
            
            print(f"   Testing with objects:")
            for obj in test_objects:
                print(f"     - {obj['name']} ({obj['role']})")
            
            extracted = await detection.extract_contents(
                test_url,
                test_objects,
                include_snippets=True
            )
            
            print(f"\n   Successfully extracted content for {len(extracted)} objects")
            
            # Show detailed results
            for i, content in enumerate(extracted):
                print(f"\n   Object {i+1}:")
                print(f"     Name: {content.get('object_name')}")
                print(f"     Type: {content.get('object_type')}")
                print(f"     URL: {content.get('url')}")
                
                signature = content.get('signature', '')
                if signature:
                    clean_sig = signature.replace('\n', ' ').strip()
                    print(f"     Signature: {clean_sig[:100]}{'...' if len(clean_sig) > 100 else ''}")
                
                description = content.get('description', '')
                if description:
                    clean_desc = description.replace('\n', ' ').strip()
                    print(f"     Description: {clean_desc[:150]}{'...' if len(clean_desc) > 150 else ''}")
                
                snippet = content.get('content_snippet', '')
                if snippet:
                    clean_snippet = snippet.replace('\n', ' ').strip()
                    print(f"     Snippet: {clean_snippet[:100]}{'...' if len(clean_snippet) > 100 else ''}")
        else:
            print("   No inventory objects found to test with")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


async def test_theme_patterns():
    """Test theme pattern selection."""
    print("\nTesting theme patterns...\n")
    
    from librovore.structures.mkdocs.extraction import MATERIAL_THEME_PATTERNS, _GENERIC_PATTERN
    
    themes = ['material', 'readthedocs', 'unknown']
    
    for theme in themes:
        print(f"Theme: {theme}")
        patterns = MATERIAL_THEME_PATTERNS.get(theme, _GENERIC_PATTERN)
        
        print(f"  Main content selectors: {len(patterns['main_content_selectors'])}")
        print(f"  API section selectors: {len(patterns['api_section_selectors'])}")
        print(f"  Description selectors: {len(patterns['description_selectors'])}")
        print(f"  Cleanup selectors: {len(patterns['cleanup_selectors'])}")
        print()


async def main():
    """Main test routine."""
    try:
        await test_theme_patterns()
        await test_mkdocs_processor_direct()
        print("\n✓ Direct MkDocs processor testing completed successfully")
        
    except Exception as e:
        print(f"\n✗ Testing failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    asyncio.run(main())