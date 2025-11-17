#!/usr/bin/env python3

import sys
sys.path.insert(0, 'sources')

from sphinxmcps.processors.sphinx.conversion import html_to_markdown

# Test with typical Sphinx HTML content that would cause 'walls of text'
html = '''<p>This is the first paragraph with some <strong>bold text</strong> and <em>italic text</em>.</p>
<p>This is the second paragraph that should be separate from the first.</p>
<p>Here is a third paragraph with a <a href="http://example.com">link</a> inside.</p>
<div class="highlight"><pre><code>def example():
    return 'code block'</code></pre></div>
<p>Final paragraph after code block.</p>'''

result = html_to_markdown(html)
print('=== Current conversion result ===')
print(repr(result))
print()
print('=== How it looks when printed ===')
print(result)
print()

# Test with more complex HTML that might cause issues
complex_html = '''<div class="section">
<p>Introduction paragraph with some text.</p>
<div class="admonition note">
<p class="admonition-title">Note</p>
<p>This is a note block that should be formatted nicely.</p>
</div>
<p>Another paragraph after the note.</p>
<ul>
<li>First list item</li>
<li>Second list item with <code>inline code</code></li>
<li>Third item</li>
</ul>
<p>Paragraph after list.</p>
</div>'''

result2 = html_to_markdown(complex_html)
print('=== Complex HTML conversion ===')
print(repr(result2))
print()
print('=== How it looks when printed ===')
print(result2)