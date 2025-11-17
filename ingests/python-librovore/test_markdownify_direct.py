#!/usr/bin/env python3

from librovore.structures.sphinx.conversion import html_to_markdown

# Test with complex HTML that might come from Python docs
test_html = '''
<div class="section">
<h2>Dictionary Methods</h2>
<p>Here are some <strong>important</strong> methods:</p>
<ul>
<li><code>dict.get()</code> - Get value for key</li>
<li><code>dict.keys()</code> - Get dictionary keys</li>
<li><code>dict.items()</code> - Get key-value pairs</li>
</ul>
<p>Example usage:</p>
<pre><code>d = {'a': 1, 'b': 2}
print(d.get('a'))  # Output: 1
</code></pre>
</div>
'''

result = html_to_markdown(test_html)
print('Result:')
print(repr(result))
print()
print('Rendered:')
print(result)
print()

# Test empty content
empty_result = html_to_markdown('')
print('Empty result:', repr(empty_result))

# Test minimal content
minimal_html = '<p>Simple text</p>'
minimal_result = html_to_markdown(minimal_html)
print('Minimal result:', repr(minimal_result))