#!/usr/bin/env python3

from bs4 import BeautifulSoup
from librovore.structures.sphinx.conversion import html_to_markdown

# Test with inner content extraction
test_html = '''
<div>
    <dt id="dict">dict</dt>
    <dd>
        <p>Return a new dictionary initialized from an optional positional argument.</p>
        <p>Dictionaries can be created by several means:</p>
        <ul>
            <li>Use a comma-separated list</li>
            <li>Use a dict comprehension</li>
        </ul>
        <p>If no positional argument is given, an empty dictionary is created.</p>
    </dd>
</div>
'''

soup = BeautifulSoup(test_html, 'lxml')
element = soup.find(id='dict')
sibling = element.find_next_sibling('dd')

print("=== METHOD 1: Full element HTML ===")
full_html = str(sibling)
markdown1 = html_to_markdown(full_html)
print("Result:")
print(repr(markdown1))

print("\n=== METHOD 2: Inner HTML only ===")
inner_html = sibling.decode_contents()
print("Inner HTML:")
print(repr(inner_html[:150]))
markdown2 = html_to_markdown(inner_html)
print("Result:")
print(repr(markdown2))
print("\nRendered:")
print(markdown2)