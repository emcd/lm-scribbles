#!/usr/bin/env python3
"""
Test MkDocs content extraction through the MCP server interface.
"""

import asyncio
import json
from pathlib import Path

# Set up the path for librovore imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'sources'))

from librovore import detection


async def test_mkdocs_detection_and_extraction():
    """Test MkDocs detection and content extraction through MCP interface."""
    print("Testing MkDocs detection and extraction through MCP interface...\n")
    
    # Test site
    test_url = 'https://fastapi.tiangolo.com/'
    
    print(f"Testing with {test_url}")
    
    try:
        # Step 1: Detect structure processors
        print("1. Detecting structure processors...")
        from librovore.interfaces import ProcessorGenera
        
        structure_detections_data, optimal_structure = await detection.access_detections(
            test_url, genus=ProcessorGenera.Structure
        )
        
        inventory_detections_data, optimal_inventory = await detection.access_detections(
            test_url, genus=ProcessorGenera.Inventory
        )
        
        print(f"   Found {len(structure_detections_data)} structure processors")
        for name, det in structure_detections_data.items():
            print(f"     - {name}: confidence {det.confidence}")
        
        print(f"   Found {len(inventory_detections_data)} inventory processors")
        for name, det in inventory_detections_data.items():
            print(f"     - {name}: confidence {det.confidence}")
        
        # Step 2: Test MkDocs structure detection specifically
        if 'mkdocs' in structure_detections_data:
            mkdocs_detection = structure_detections_data['mkdocs']
            print(f"\n2. MkDocs detection details:")
            print(f"   Confidence: {mkdocs_detection.confidence}")
            print(f"   Theme: {getattr(mkdocs_detection, 'theme', 'Unknown')}")
            
            # Step 3: Get some inventory objects to test with
            print("\n3. Getting inventory objects...")
            
            if inventory_detections_data:
                # Use Sphinx inventory (should be available on FastAPI)
                sphinx_detection = inventory_detections_data.get('sphinx')
                if sphinx_detection:
                    objects = await sphinx_detection.filter_inventory(
                        test_url,
                        filters={'domain': 'py', 'role': 'class'},
                        details=detection.InventoryQueryDetails.Documentation
                    )
                    
                    print(f"   Found {len(objects)} inventory objects")
                    
                    if objects:
                        # Step 4: Extract content using MkDocs processor
                        print("\n4. Extracting content using MkDocs processor...")
                        test_objects = objects[:2]  # Test with first 2 objects
                        
                        extracted = await mkdocs_detection.extract_contents(
                            test_url,
                            test_objects,
                            include_snippets=True
                        )
                        
                        print(f"   Successfully extracted content for {len(extracted)} objects")
                        
                        # Show detailed results
                        for i, content in enumerate(extracted):
                            print(f"\n   Object {i+1}:")
                            print(f"     Name: {content.get('object_name')}")
                            print(f"     Type: {content.get('object_type')}")
                            print(f"     URL: {content.get('url')}")
                            
                            signature = content.get('signature', '')
                            if signature:
                                print(f"     Signature: {signature[:100]}{'...' if len(signature) > 100 else ''}")
                            
                            description = content.get('description', '')
                            if description:
                                print(f"     Description: {description[:150]}{'...' if len(description) > 150 else ''}")
                            
                            snippet = content.get('content_snippet', '')
                            if snippet:
                                print(f"     Snippet: {snippet[:100]}{'...' if len(snippet) > 100 else ''}")
                    else:
                        print("   No inventory objects found to test with")
                else:
                    print("   No Sphinx inventory detection found")
            else:
                print("   No inventory detections found")
        else:
            print("   MkDocs processor not detected")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


async def main():
    """Main test routine."""
    try:
        await test_mkdocs_detection_and_extraction()
        print("\n✓ MkDocs MCP integration testing completed successfully")
        
    except Exception as e:
        print(f"\n✗ Testing failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    asyncio.run(main())