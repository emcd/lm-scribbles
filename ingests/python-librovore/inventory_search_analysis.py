#!/usr/bin/env python3
"""
Analysis script to examine the relationship between Sphinx inventories
and MkDocs search functionality.

This investigates how we can use objects.inv to guide content extraction
from MkDocs sites that have mkdocstrings.
"""

import asyncio
import json
from urllib.parse import urljoin, urlparse
import httpx
from pathlib import Path


async def check_objects_inv(base_url: str) -> dict:
    """Check if objects.inv exists and analyze its content."""
    results = {
        'base_url': base_url,
        'has_objects_inv': False,
        'objects_inv_url': None,
        'inventory_accessible': False,
        'objects_count': 0,
        'domains': set(),
        'roles': set(),
        'sample_objects': []
    }
    
    # Try common objects.inv locations
    inv_locations = [
        'objects.inv',
        'docs/objects.inv',
        'latest/objects.inv'
    ]
    
    async with httpx.AsyncClient(timeout=15.0) as client:
        for location in inv_locations:
            inv_url = urljoin(base_url, location)
            try:
                response = await client.head(inv_url)
                if response.status_code == 200:
                    results['has_objects_inv'] = True
                    results['objects_inv_url'] = inv_url
                    
                    # Try to download and analyze the inventory
                    try:
                        inv_response = await client.get(inv_url)
                        if inv_response.status_code == 200:
                            results['inventory_accessible'] = True
                            # Save the inventory for manual analysis
                            domain = urlparse(base_url).netloc.replace('.', '_')
                            inv_file = Path(__file__).parent / f'objects_{domain}.inv'
                            with inv_file.open('wb') as f:
                                f.write(inv_response.content)
                            print(f"  Saved inventory to {inv_file}")
                            
                    except Exception as e:
                        print(f"  Error downloading inventory: {e}")
                    
                    break
                    
            except Exception as e:
                continue  # Try next location
    
    return results


async def analyze_search_index_structure(search_index_url: str) -> dict:
    """Analyze the structure of a search index to understand content organization."""
    results = {
        'url': search_index_url,
        'accessible': False,
        'config': {},
        'document_count': 0,
        'sample_locations': [],
        'content_patterns': set()
    }
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(search_index_url)
            if response.status_code == 200:
                results['accessible'] = True
                data = response.json()
                
                if 'config' in data:
                    results['config'] = data['config']
                
                if 'docs' in data:
                    docs = data['docs']
                    results['document_count'] = len(docs)
                    
                    # Sample first 5 documents for analysis
                    for i, doc in enumerate(docs[:5]):
                        location = doc.get('location', '')
                        title = doc.get('title', '')
                        text_preview = doc.get('text', '')[:100] + '...'
                        
                        results['sample_locations'].append({
                            'location': location,
                            'title': title,
                            'text_preview': text_preview
                        })
                        
                        # Look for content patterns that might correspond to API objects
                        if any(pattern in title.lower() for pattern in 
                               ['class', 'function', 'method', 'module', 'api']):
                            results['content_patterns'].add('api_documentation')
                        
                        if 'tutorial' in location.lower() or 'guide' in location.lower():
                            results['content_patterns'].add('tutorial_content')
                            
                        if 'reference' in location.lower():
                            results['content_patterns'].add('reference_content')
                    
                    results['content_patterns'] = list(results['content_patterns'])
                    
        except Exception as e:
            print(f"  Error analyzing search index: {e}")
    
    return results


async def main():
    """Main analysis routine."""
    sites = [
        'https://docs.pydantic.dev/latest/',
        'https://fastapi.tiangolo.com/',
        'https://mkdocstrings.github.io/'
    ]
    
    print("Analyzing inventory and search index relationships...\n")
    
    all_results = {}
    
    for site in sites:
        print(f"Analyzing {site}...")
        
        # Check for objects.inv
        inv_results = await check_objects_inv(site)
        
        # Analyze search index
        search_index_url = urljoin(site, 'search/search_index.json')
        search_results = await analyze_search_index_structure(search_index_url)
        
        all_results[site] = {
            'inventory': inv_results,
            'search_index': search_results
        }
        
        print(f"  Objects.inv: {'✓' if inv_results['has_objects_inv'] else '✗'}")
        if inv_results['has_objects_inv']:
            print(f"    URL: {inv_results['objects_inv_url']}")
        
        print(f"  Search index: {'✓' if search_results['accessible'] else '✗'}")
        if search_results['accessible']:
            print(f"    Documents: {search_results['document_count']}")
            print(f"    Content patterns: {search_results['content_patterns']}")
        
        print()
    
    # Save results
    output_file = Path(__file__).parent / 'inventory_search_analysis.json'
    with output_file.open('w') as f:
        json.dump(all_results, f, indent=2, default=str)
    
    print(f"Analysis saved to {output_file}")


if __name__ == '__main__':
    asyncio.run(main())