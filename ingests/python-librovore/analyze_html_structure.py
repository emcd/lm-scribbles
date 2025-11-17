#!/usr/bin/env python3

import sys
import asyncio
sys.path.insert(0, 'sources')

async def analyze_html_structure():
    """Analyze HTML structure of remote vs local sites"""
    from sphinxmcps.cacheproxy import retrieve_url_as_text
    from sphinxmcps.processors.sphinx import urls as _urls
    from bs4 import BeautifulSoup
    
    sites = [
        ('https://docs.python.org/3/', 'library/asyncio.html#module-$', 'module-asyncio', 'Python docs'),
        ('.auxiliary/artifacts/sphinx-html', 'api.html#$', 'sphinxmcps.cacheproxy.ProbeResponse', 'Local site')
    ]
    
    for source, uri, anchor, name in sites:
        print(f"\n=== Analyzing {name} ===")
        
        base_url = _urls.normalize_base_url(source)
        doc_url = _urls.derive_documentation_url(base_url, uri, anchor)
        
        print(f"URL: {doc_url.geturl()}")
        print(f"Looking for anchor: {anchor}")
        
        try:
            html_content = await retrieve_url_as_text(doc_url)
            soup = BeautifulSoup(html_content, 'lxml')
            
            # Check for main content containers
            main_article = soup.find('article', {'role': 'main'})
            main_div = soup.find('div', {'class': 'main'})
            main_section = soup.find('main')
            content_div = soup.find('div', {'id': 'furo-main-content'})
            
            print(f"  <article role='main'>: {'Found' if main_article else 'Not found'}")
            print(f"  <div class='main'>: {'Found' if main_div else 'Not found'}")
            print(f"  <main>: {'Found' if main_section else 'Not found'}")
            print(f"  <div id='furo-main-content'>: {'Found' if content_div else 'Not found'}")
            
            # Check for the specific anchor
            target_element = soup.find(id=anchor)
            print(f"  Target element #{anchor}: {'Found' if target_element else 'Not found'}")
            
            if target_element:
                print(f"    Tag: {target_element.name}")
                print(f"    Classes: {target_element.get('class', [])}")
                print(f"    Parent: {target_element.parent.name if target_element.parent else 'None'}")
            
            # Look for similar anchors
            similar_anchors = soup.find_all(id=lambda x: x and 'asyncio' in x if anchor == 'module-asyncio' else (x and 'ProbeResponse' in x))
            if similar_anchors:
                print(f"  Similar anchors found: {[elem.get('id') for elem in similar_anchors[:3]]}")
                
        except Exception as e:
            print(f"  Error: {e}")

if __name__ == '__main__':
    asyncio.run(analyze_html_structure())