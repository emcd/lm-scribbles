#!/usr/bin/env python3

from bs4 import BeautifulSoup
from librovore.structures.sphinx.conversion import html_to_markdown

# Test HTML that simulates Python docs structure
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

print("=== CURRENT METHOD (get_text) ===")
plain_text = sibling.get_text()
print("Plain text:")
print(repr(plain_text))
print("\nAfter html_to_markdown:")
markdown_from_text = html_to_markdown(plain_text)
print(repr(markdown_from_text))

print("\n=== PROPOSED METHOD (preserve HTML) ===")
html_content = str(sibling)
print("HTML content:")
print(repr(html_content[:200]))
print("\nAfter html_to_markdown:")
markdown_from_html = html_to_markdown(html_content)
print(repr(markdown_from_html))
print("\nRendered:")
print(markdown_from_html)