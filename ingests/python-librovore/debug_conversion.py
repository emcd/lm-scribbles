#!/usr/bin/env python3

import sys
sys.path.insert(0, 'sources')

from bs4 import BeautifulSoup
from sphinxmcps.processors.sphinx.conversion import html_to_markdown

# Debug the conversion process step by step
def debug_conversion():
    sphinx_html = '''
    <dt class="sig sig-object py" id="example.function">
    <span class="sig-prename descclassname"><span class="pre">example.</span></span><span class="sig-name descname"><span class="pre">function</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">param1</span></span></em>, <em class="sig-param"><span class="n"><span class="pre">param2</span></span><span class="o"><span class="pre">=</span></span><span class="default_value"><span class="pre">None</span></span></em><span class="sig-paren">)</span><a class="headerlink" href="#example.function" title="Link to this definition">¶</a></dt>
    <dd>
    <p>This is the first paragraph of documentation for this function. It explains what the function does in some detail.</p>
    <p>This is a second paragraph that should be separate from the first paragraph. It provides additional information about usage.</p>
    <div class="admonition note">
    <p class="admonition-title">Note</p>
    <p>This is an important note that users should pay attention to. It contains critical information about the function's behavior.</p>
    </div>
    <p>After the note, we have another paragraph that continues the documentation.</p>
    </dd>
    '''
    
    print("=== Step by step debugging ===")
    
    # Step 1: Parse HTML
    soup = BeautifulSoup(sphinx_html, 'lxml')
    print("Step 1 - Original HTML structure:")
    print(f"Found {len(soup.find_all('p'))} paragraph elements")
    print(f"Found {len(soup.find_all('div'))} div elements")
    print()
    
    # Step 2: Clean navigation
    for header_link in soup.find_all('a', class_='headerlink'):
        header_link.decompose()
    print("Step 2 - After cleaning navigation")
    print()
    
    # Step 3: Check block elements before processing
    block_elements = ['p', 'div', 'section', 'article', 'li', 'dt', 'dd', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    print("Step 3 - Block elements found:")
    for element_name in block_elements:
        elements = soup.find_all(element_name)
        if elements:
            print(f"  {element_name}: {len(elements)} elements")
            for i, elem in enumerate(elements):
                text = elem.get_text(strip=True)
                print(f"    {i+1}: '{text[:50]}...' ({len(text)} chars)")
    print()
    
    # Step 4: Process inline elements first (like current code)
    for code in soup.find_all('code'):
        code.replace_with(f"`{code.get_text()}`")
    for pre in soup.find_all('pre'):
        pre.replace_with(f"```\n{pre.get_text()}\n```")
    for strong in soup.find_all('strong'):
        strong.replace_with(f"**{strong.get_text()}**")
    for em in soup.find_all('em'):
        em.replace_with(f"*{em.get_text()}*")
    for link in soup.find_all('a'):
        href = link.get('href', '')
        text = link.get_text()
        if href: link.replace_with(f"[{text}]({href})")
        else: link.replace_with(text)
    
    print("Step 4 - After processing inline elements:")
    print(f"Found {len(soup.find_all('p'))} paragraph elements remaining")
    print()
    
    # Step 5: Try to get text with default separator
    text_default = soup.get_text(separator=' ')
    print("Step 5 - get_text() with default separator:")
    print(f"Result: {repr(text_default[:200])}...")
    print()
    
    # Step 6: Try to get text with custom separator for each block element
    separator = '***PARA***'
    for element_name in ['p', 'div']:
        for element in soup.find_all(element_name):
            element_text = element.get_text(strip=True)
            if element_text:
                element.replace_with(element_text + separator)
    
    text_custom = soup.get_text(separator=' ')
    print("Step 6 - After adding custom separators:")
    print(f"Raw result: {repr(text_custom[:200])}...")
    print()
    
    # Step 7: Replace separators
    final_text = text_custom.replace(separator, '\n\n')
    print("Step 7 - After replacing separators:")
    print(f"Final result: {repr(final_text[:200])}...")
    print()
    print("Number of paragraph breaks:", final_text.count('\n\n'))

if __name__ == '__main__':
    debug_conversion()