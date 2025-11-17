#!/usr/bin/env python3

from librovore.structures.sphinx.conversion import html_to_markdown

# Test HTML with multiple paragraphs
test_html = '''
<div>
<p>First paragraph with some content.</p>
<p>Second paragraph that should be separated from the first.</p>
<p>Third paragraph with <strong>bold text</strong> and more content.</p>
<ul>
<li>First list item</li>
<li>Second list item</li>
</ul>
<p>Fourth paragraph after the list.</p>
</div>
'''

result = html_to_markdown(test_html)
print("Current output:")
print(repr(result))
print()
print("Rendered:")
print(result)
print()

# Test with more complex structure
complex_html = '''
<div>
<h2>Section Header</h2>
<p>Introduction paragraph.</p>

<p>Paragraph with code: <code>dict.get()</code> method.</p>

<pre><code>example_code = {
    'key': 'value'
}
</code></pre>

<p>Final paragraph with explanation.</p>
</div>
'''

complex_result = html_to_markdown(complex_html)
print("Complex structure:")
print(repr(complex_result))
print()
print("Rendered:")
print(complex_result)