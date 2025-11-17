#!/usr/bin/env python3

import sys
import re
sys.path.insert(0, 'sources')

def _clean_whitespace_debug(text: str) -> str:
    """Debug version of the whitespace cleaning function"""
    print(f"Input text (first 200 chars): {repr(text[:200])}")
    double_newlines = text.count('\n\n')
    print(f"Input paragraph breaks: {double_newlines}")
    
    # Multiple spaces to single space
    text = re.sub(r' +', ' ', text)
    double_newlines = text.count('\n\n')
    print(f"After space cleanup: {double_newlines} paragraph breaks")
    
    # Remove leading spaces on lines
    text = re.sub(r'\n +', '\n', text)
    double_newlines = text.count('\n\n')
    print(f"After leading space cleanup: {double_newlines} paragraph breaks")
    
    # Remove trailing spaces on lines
    text = re.sub(r' +\n', '\n', text)
    double_newlines = text.count('\n\n')
    print(f"After trailing space cleanup: {double_newlines} paragraph breaks")
    
    # Multiple newlines to double newlines
    text = re.sub(r'\n{3,}', '\n\n', text)
    double_newlines = text.count('\n\n')
    print(f"After multiple newline cleanup: {double_newlines} paragraph breaks")
    
    # Remove leading/trailing whitespace on each line
    text = re.sub(r'^\s+|\s+$', '', text, flags=re.MULTILINE)
    double_newlines = text.count('\n\n')
    print(f"After line trim: {double_newlines} paragraph breaks")
    
    result = text.strip()
    double_newlines = result.count('\n\n')
    print(f"Final result paragraph breaks: {double_newlines}")
    print(f"Final result (first 200 chars): {repr(result[:200])}")
    
    return result

# Test with text that has paragraph breaks
test_text = """example.function(*param1*,*param2=None*)

This is the first paragraph of documentation for this function. It explains what the function does in some detail.

This is a second paragraph that should be separate from the first paragraph. It provides additional information about usage.

After the note, we have another paragraph that continues the documentation."""

print("=== Testing whitespace cleaning ===")
cleaned = _clean_whitespace_debug(test_text)
print()
print("=== Final result ===")
print(cleaned)