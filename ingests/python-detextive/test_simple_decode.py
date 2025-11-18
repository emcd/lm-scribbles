#!/usr/bin/env python3
import sys
sys.path.insert(0, 'sources')
import detextive

# Test basic decode functionality
content = b'Hello, world!'
try:
    text = detextive.decode(content)
    print(f'SUCCESS: {text}')
except Exception as e:
    print(f'ERROR: {type(e).__name__}: {e}')

# Try with specific mimetype hint
try:
    text = detextive.decode(content, mimetype_supplement='text/plain')
    print(f'WITH SUPPLEMENT: {text}')
except Exception as e:
    print(f'SUPPLEMENT ERROR: {type(e).__name__}: {e}')

# Test the confidence API
try:
    mimetype_result, charset_result = detextive.infer_mimetype_charset_confidence(content)
    print(f'CONFIDENCE API: {mimetype_result.value} (conf: {mimetype_result.confidence:.3f}), {charset_result.value if charset_result else None} (conf: {charset_result.confidence:.3f if charset_result else "N/A"})')
except Exception as e:
    print(f'CONFIDENCE ERROR: {type(e).__name__}: {e}')

# Check what happens with empty content
empty = b''
try:
    text = detextive.decode(empty)
    print(f'EMPTY SUCCESS: "{text}"')
except Exception as e:
    print(f'EMPTY ERROR: {type(e).__name__}: {e}')