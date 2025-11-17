#!/usr/bin/env python3

import asyncio
from librovore import functions as _functions
from librovore.state import Globals
from librovore.structures.sphinx.conversion import html_to_markdown

async def debug_paragraph_pipeline():
    """Debug the paragraph spacing through the entire pipeline."""
    
    # Initialize globals (minimal setup)
    auxdata = Globals()
    
    print("=== DEBUGGING PARAGRAPH PIPELINE ===\n")
    
    # Query for dict documentation  
    try:
        result = await _functions.query_content(
            auxdata, 
            'https://docs.python.org/3', 
            'dict',
            results_max=1,
            include_snippets=True
        )
        
        if 'documents' in result and result['documents']:
            doc = result['documents'][0]
            description = doc.get('description', '')
            
            print("1. FINAL DESCRIPTION (what we see in CLI):")
            print("Length:", len(description))
            print("First 500 chars:")
            print(repr(description[:500]))
            print("\nRendered preview:")
            print(description[:500])
            print("\n" + "="*60 + "\n")
            
            # Let's see if we can trace back to the original HTML
            # We'll need to look at the extraction process more directly
            
    except Exception as e:
        print(f"Error in query: {e}")

if __name__ == "__main__":
    asyncio.run(debug_paragraph_pipeline())