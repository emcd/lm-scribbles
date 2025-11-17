#!/usr/bin/env python3

import markdownify
from bs4 import BeautifulSoup

# Test HTML that simulates MkDocs structure with Material theme
test_html = '''
<div class="doc-contents">
    <p>Return a new dictionary initialized from an optional positional argument.</p>
    <p>Dictionaries can be created by several means:</p>
    <ul>
        <li>Use a comma-separated list of key-value pairs</li>
        <li>Use a dict comprehension: <code>{x: x**2 for x in (2, 4, 6)}</code></li>
        <li>Use the type constructor: <code>dict()</code></li>
    </ul>
    <p>If no positional argument is given, an empty dictionary is created.</p>
    <div class="admonition tip">
        <p class="admonition-title">Tip</p>
        <p>Dictionary comprehensions are often the most readable way to create dictionaries.</p>
    </div>
</div>
'''

soup = BeautifulSoup(test_html, 'lxml')
doc_contents = soup.find(class_='doc-contents')

print("=== NEW IMPROVED METHOD (full content + markdownify) ===")

# Extract full inner HTML from doc-contents
full_inner_html = doc_contents.decode_contents()
print("Inner HTML:")
print(repr(full_inner_html[:150]) + "...")

# Convert to markdown
markdown_result = markdownify.markdownify(full_inner_html, heading_style='ATX')

print("\nMarkdownify result:")
print(repr(markdown_result))

print("\nRendered:")
print(markdown_result)