#!/usr/bin/env python3

import asyncio
import librovore.structures.mkdocs as mkdocs_proc
import librovore.structures.sphinx as sphinx_proc

# Register both processors
mkdocs_proc.register({})
sphinx_proc.register({})

async def test_processors():
    # Test with multiple sites
    sites = [
        ('FastAPI (MkDocs+mkdocstrings)', 'https://fastapi.tiangolo.com'),
        ('HTTPX (Sphinx)', 'https://www.python-httpx.org'),
        ('Pydantic (MkDocs+mkdocstrings)', 'https://docs.pydantic.dev'),
    ]
    
    # Create processors
    from librovore.xtnsapi import processors
    print('Available processors:', list(processors.keys()))
    
    mkdocs_processor = processors.get('mkdocs')
    sphinx_processor = processors.get('sphinx')
    
    for site_name, site_url in sites:
        print(f'\n=== Testing {site_name} ===')
        
        if mkdocs_processor:
            print('\nMkDocs processor:')
            mkdocs_detection = await mkdocs_processor.detect(site_url)
            print(f'  Confidence: {mkdocs_detection.confidence}')
            print(f'  Has objects.inv: {mkdocs_detection.has_objects_inv}')
            print(f'  Has mkdocs.yml: {mkdocs_detection.has_mkdocs_yml}')
            print(f'  Theme: {mkdocs_detection.theme}')
        
        if sphinx_processor:
            print('\nSphinx processor:')
            sphinx_detection = await sphinx_processor.detect(site_url)
            print(f'  Confidence: {sphinx_detection.confidence}')
            print(f'  Has objects.inv: {sphinx_detection.has_objects_inv}')
            print(f'  Has searchindex: {sphinx_detection.has_searchindex}')
            print(f'  Theme: {sphinx_detection.theme}')

if __name__ == '__main__':
    asyncio.run(test_processors())