#!/usr/bin/env python3

import sys
import asyncio
sys.path.insert(0, 'sources')

async def analyze_theme_markers():
    """Analyze HTML content to identify theme markers"""
    from sphinxmcps.cacheproxy import retrieve_url_as_text
    from sphinxmcps.processors.sphinx import urls as _urls
    
    sites = [
        ('https://docs.python.org/3/', 'Python docs'),
        ('https://flask.palletsprojects.com/en/stable/', 'Flask docs'),
    ]
    
    for source, name in sites:
        print(f"\n=== Analyzing {name} ===")
        
        base_url = _urls.normalize_base_url(source)
        html_url = _urls.derive_html_url(base_url)
        
        try:
            html_content = await retrieve_url_as_text(html_url, duration_max=10.0)
            html_lower = html_content.lower()
            
            print(f"URL: {html_url.geturl()}")
            print(f"HTML length: {len(html_content)}")
            
            # Check for various theme indicators
            theme_indicators = {
                'furo': ['furo', 'css/furo.css'],
                'sphinx_rtd_theme': ['sphinx_rtd_theme', 'rtd_theme', 'css/theme.css'],
                'alabaster': ['alabaster', 'css/alabaster.css'],
                'nature': ['css/nature.css', 'nature'],
                'haiku': ['css/haiku.css', 'haiku'],
                'agogo': ['css/agogo.css', 'agogo'],
                'traditional': ['css/traditional.css'],
                'epub': ['epub'],
                'bizstyle': ['css/bizstyle.css'],
                'classic': ['css/default.css', 'css/classic.css'],
                'sphinx_book_theme': ['sphinx_book_theme', 'book_theme'],
                'pydata_sphinx_theme': ['pydata_sphinx_theme', 'pydata'],
            }
            
            detected_themes = []
            for theme_name, indicators in theme_indicators.items():
                for indicator in indicators:
                    if indicator in html_lower:
                        detected_themes.append(f"{theme_name} (found: {indicator})")
                        break
            
            if detected_themes:
                print("Detected themes:")
                for theme in detected_themes:
                    print(f"  - {theme}")
            else:
                print("No known themes detected")
                
            # Look for CSS files and generator meta tags
            import re
            css_links = re.findall(r'<link[^>]*href=["\']([^"\']*\.css[^"\']*)["\']', html_content, re.IGNORECASE)
            generator_meta = re.findall(r'<meta[^>]*name=["\']generator["\'][^>]*content=["\']([^"\']*)["\']', html_content, re.IGNORECASE)
            
            print(f"CSS files found: {len(css_links)}")
            for css in css_links[:5]:  # Show first 5
                print(f"  - {css}")
            if len(css_links) > 5:
                print(f"  ... and {len(css_links) - 5} more")
                
            if generator_meta:
                print(f"Generator meta tags: {generator_meta}")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    asyncio.run(analyze_theme_markers())