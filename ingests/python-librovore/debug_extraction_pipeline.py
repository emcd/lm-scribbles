#!/usr/bin/env python3

import asyncio
from librovore import functions as _functions
from librovore.state import Globals

async def debug_extraction_pipeline():
    """Debug the entire extraction pipeline for Pydantic BaseModel."""
    
    auxdata = Globals()
    
    print("=== DEBUGGING FULL EXTRACTION PIPELINE ===")
    
    try:
        result = await _functions.query_content(
            auxdata, 
            'https://docs.pydantic.dev/latest/', 
            'BaseModel',
            results_max=1,
            include_snippets=True
        )
        
        print(f"Result keys: {list(result.keys())}")
        
        if 'documents' in result and result['documents']:
            doc = result['documents'][0]
            print(f"Document keys: {list(doc.keys())}")
            
            description = doc.get('description', '')
            print(f"Description type: {type(description)}")
            print(f"Description length: {len(description)}")
            
            # Check first few lines
            if description:
                lines = description.split('\n')
                print(f"Number of lines: {len(lines)}")
                print("First 5 lines:")
                for i, line in enumerate(lines[:5], 1):
                    print(f"  {i}: {repr(line)}")
                
                # Also check if it's being truncated somewhere else
                print(f"\nLast 5 lines:")
                for i, line in enumerate(lines[-5:], len(lines)-4):
                    print(f"  {i}: {repr(line)}")
            else:
                print("Description is empty!")
                
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_extraction_pipeline())