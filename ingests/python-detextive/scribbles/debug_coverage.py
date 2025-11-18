#!/usr/bin/env python3

import detextive.detection as d
from unittest.mock import patch

# Test what happens with various charset/content combinations
test_cases = [
    ('ascii', b'\xff\xfe'),  # Invalid ASCII
    ('utf-8', b'\xff\xfe'),  # Invalid UTF-8  
    ('invalid-charset', b'valid'),  # Invalid charset name
    ('utf-8', ('\x01' * 100).encode('utf-8')),  # Valid decode, unreasonable content
]

for charset, content in test_cases:
    with patch('puremagic.from_string') as mock_puremagic, \
         patch('mimetypes.guess_type') as mock_mimetypes, \
         patch('chardet.detect') as mock_chardet:
        
        mock_puremagic.side_effect = ValueError("No magic")
        mock_mimetypes.return_value = (None, None)
        mock_chardet.return_value = {'encoding': charset}
        
        try:
            result = d.detect_mimetype_and_charset(content, 'test')
            print(f"charset={charset}, content={content[:20]!r} -> {result}")
        except Exception as e:
            print(f"charset={charset}, content={content[:20]!r} -> Exception: {type(e).__name__}: {e}")