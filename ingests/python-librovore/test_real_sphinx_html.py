#!/usr/bin/env python3

import sys
sys.path.insert(0, 'sources')

# Get some real Sphinx HTML content to test conversion
def test_with_real_sphinx_html():
    """Test HTML-to-Markdown conversion with real Sphinx HTML"""
    
    # Example of typical Sphinx HTML that would cause "walls of text"
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
    <div class="highlight-python notranslate">
    <div class="highlight">
    <pre><span></span><span class="c1"># Example usage:</span>
    <span class="n">result</span> <span class="o">=</span> <span class="n">example</span><span class="o">.</span><span class="n">function</span><span class="p">(</span><span class="s2">&quot;hello&quot;</span><span class="p">)</span>
    <span class="nb">print</span><span class="p">(</span><span class="n">result</span><span class="p">)</span>
    </pre>
    </div>
    </div>
    <p>Final paragraph after the code example.</p>
    </dd>
    '''
    
    from sphinxmcps.processors.sphinx.conversion import html_to_markdown
    
    result = html_to_markdown(sphinx_html)
    
    print("=== Real Sphinx HTML conversion ===")
    print("Input HTML length:", len(sphinx_html))
    print()
    print("=== Raw result ===")
    print(repr(result))
    print()
    print("=== Formatted result ===")
    print(result)
    print()
    print("=== Analysis ===")
    lines = result.split('\n')
    print(f"Number of lines: {len(lines)}")
    
    # Count paragraph breaks (double newlines)
    double_newlines = result.count('\n\n')
    print(f"Number of paragraph breaks: {double_newlines}")
    
    # Look for proper spacing
    if double_newlines == 0:
        print("❌ PROBLEM: No paragraph breaks found - this is the 'wall of text' issue!")
    else:
        print(f"✅ Found {double_newlines} paragraph breaks")

if __name__ == '__main__':
    test_with_real_sphinx_html()