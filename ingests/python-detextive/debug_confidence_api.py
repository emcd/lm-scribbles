#!/usr/bin/env python3
"""
Debug the confidence API failure.
"""
import sys
sys.path.insert(0, 'sources')
import detextive

content = b'Hello, world!'
print(f"Testing content: {content}")

# Try charset detection first
try:
    charset = detextive.detect_charset(content)
    print(f"Charset detection: {charset}")
except Exception as e:
    print(f"Charset detection error: {type(e).__name__}: {e}")

# Try MIME type detection
try:
    mimetype = detextive.detect_mimetype(content)
    print(f"MIME type detection: {mimetype}")
except Exception as e:
    print(f"MIME type detection error: {type(e).__name__}: {e}")

# Try MIME type detection with charset hint
try:
    charset = detextive.detect_charset(content) or 'utf-8'
    mimetype = detextive.detect_mimetype(content, charset=charset)
    print(f"MIME type with charset hint: {mimetype}")
except Exception as e:
    print(f"MIME type with charset error: {type(e).__name__}: {e}")

# Test the combined inference
try:
    mimetype, charset = detextive.infer_mimetype_charset(content)
    print(f"Combined inference: {mimetype}, {charset}")
except Exception as e:
    print(f"Combined inference error: {type(e).__name__}: {e}")

# Test mimetype supplement
try:
    mimetype, charset = detextive.infer_mimetype_charset(
        content, mimetype_supplement='text/plain')
    print(f"With mimetype supplement: {mimetype}, {charset}")
except Exception as e:
    print(f"With supplement error: {type(e).__name__}: {e}")