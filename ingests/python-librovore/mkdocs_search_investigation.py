#!/usr/bin/env python3
"""
Investigation script for MkDocs search mechanisms.

This script helps us understand how Material for MkDocs implements search
so we can create a Python equivalent for librovore.
"""

import asyncio
import json
from urllib.parse import urljoin, urlparse
import httpx
from pathlib import Path


async def investigate_mkdocs_search(base_url: str) -> dict:
    """Investigate MkDocs search implementation for a given site."""
    results = {
        'base_url': base_url,
        'search_assets': [],
        'search_index_files': [],
        'search_config': {},
        'errors': []
    }
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            # Get main page to find search assets
            response = await client.get(base_url)
            html_content = response.text
            
            # Look for search-related JavaScript files
            import re
            js_pattern = r'(?:src|href)=["\']([^"\']*(?:search|worker)[^"\']*\.js[^"\']*)["\']'
            js_matches = re.findall(js_pattern, html_content, re.IGNORECASE)
            
            for js_file in js_matches:
                full_url = urljoin(base_url, js_file)
                results['search_assets'].append(full_url)
            
            # Look for search index files (common patterns)
            index_patterns = [
                'search/search_index.json',
                'assets/search/search_index.json',
                'search_index.json',
                'assets/javascripts/search_index.json'
            ]
            
            for pattern in index_patterns:
                index_url = urljoin(base_url, pattern)
                try:
                    index_response = await client.head(index_url)
                    if index_response.status_code == 200:
                        results['search_index_files'].append(index_url)
                except Exception as e:
                    pass  # Expected for most URLs
            
            # Look for manifest or config files
            config_patterns = [
                'manifest.json',
                'search.json',
                'assets/manifest.json'
            ]
            
            for pattern in config_patterns:
                config_url = urljoin(base_url, pattern)
                try:
                    config_response = await client.get(config_url)
                    if config_response.status_code == 200:
                        try:
                            config_data = config_response.json()
                            results['search_config'][pattern] = config_data
                        except json.JSONDecodeError:
                            pass
                except Exception as e:
                    pass
                    
        except Exception as e:
            results['errors'].append(f"Error investigating {base_url}: {e}")
    
    return results


async def main():
    """Main investigation routine."""
    sites = [
        'https://docs.pydantic.dev/latest/',
        'https://fastapi.tiangolo.com/',
        'https://mkdocstrings.github.io/'
    ]
    
    print("Investigating MkDocs search implementations...\n")
    
    all_results = {}
    
    for site in sites:
        print(f"Investigating {site}...")
        results = await investigate_mkdocs_search(site)
        all_results[site] = results
        
        print(f"  Search assets found: {len(results['search_assets'])}")
        for asset in results['search_assets']:
            print(f"    - {asset}")
        
        print(f"  Search index files: {len(results['search_index_files'])}")
        for index_file in results['search_index_files']:
            print(f"    - {index_file}")
        
        print(f"  Config files: {len(results['search_config'])}")
        for config_name in results['search_config']:
            print(f"    - {config_name}")
        
        if results['errors']:
            print(f"  Errors: {results['errors']}")
        
        print()
    
    # Save results for further analysis
    output_file = Path(__file__).parent / 'mkdocs_search_results.json'
    with output_file.open('w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"Results saved to {output_file}")


if __name__ == '__main__':
    asyncio.run(main())