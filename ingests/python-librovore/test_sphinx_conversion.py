#!/usr/bin/env python3

from librovore.structures.sphinx.conversion import html_to_markdown

# Test basic HTML conversion
html = '<p>This is a <strong>test</strong> with <code>inline code</code>.</p>'
result = html_to_markdown(html)
print('Basic HTML test:')
print(repr(result))
print()

# Test code block with language
html_code = '''<pre class="highlight-python"><code>def hello():
    print("Hello, world!")
</code></pre>'''
result_code = html_to_markdown(html_code)
print('Code block test:')
print(repr(result_code))
print()

# Test headerlink removal
html_header = '<h2>Section Title<a class="headerlink" href="#section">¶</a></h2>'
result_header = html_to_markdown(html_header)
print('Headerlink removal test:')
print(repr(result_header))
print()

# Test complex HTML with multiple elements
html_complex = '''
<div>
    <h3>API Reference</h3>
    <p>This function does something <em>important</em>.</p>
    <pre class="language-json"><code>{"key": "value", "number": 42}</code></pre>
    <ul>
        <li>First item</li>
        <li>Second item with <strong>bold</strong> text</li>
    </ul>
</div>
'''
result_complex = html_to_markdown(html_complex)
print('Complex HTML test:')
print(repr(result_complex))