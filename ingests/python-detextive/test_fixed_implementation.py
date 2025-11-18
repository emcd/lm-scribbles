#!/usr/bin/env python3
"""
Test the fixed implementation to verify it works correctly.
"""
import sys
sys.path.insert(0, 'sources')
import detextive

# Test cases that previously caused false positives
false_positive_cases = [
    (b'\x00\x01\x02', "Binary data that UTF-8 can decode"),
    (b'\x00' * 50, "Null bytes that UTF-8 accepts"),
]

# Test cases that should work
legitimate_cases = [
    (b'Hello, world!', "Basic ASCII text"),
    (b'Caf\xc3\xa9 \xe2\x98\x85', "UTF-8 with Unicode"),
    (b'{"message": "Hello"}', "JSON content"),
]

print("=== TESTING FIXED IMPLEMENTATION ===")

print("\n--- Cases that should NOT be detected as text/plain ---")
for content, description in false_positive_cases:
    print(f"\nCase: {description}")
    try:
        text = detextive.decode(content)
        print(f"  ERROR: Decoded as text: {repr(text[:20])}")
    except detextive.exceptions.MimetypeDetectFailure:
        print(f"  CORRECT: MimetypeDetectFailure (as expected)")
    except detextive.exceptions.ContentDecodeImpossibility:
        print(f"  CORRECT: ContentDecodeImpossibility (as expected)")
    except Exception as e:
        print(f"  UNEXPECTED: {type(e).__name__}: {e}")

print("\n--- Cases that should work ---")
for content, description in legitimate_cases:
    print(f"\nCase: {description}")
    try:
        text = detextive.decode(content)
        print(f"  SUCCESS: {repr(text)}")
    except Exception as e:
        print(f"  ERROR: {type(e).__name__}: {e}")

print("\n--- Testing confidence API ---")
test_content = b'Hello, world!'
try:
    mimetype_result, charset_result = detextive.infer_mimetype_charset_confidence(test_content)
    print(f"Confidence API works:")
    print(f"  MIME: {mimetype_result.value} (conf: {mimetype_result.confidence:.3f})")
    if charset_result:
        print(f"  Charset: {charset_result.value} (conf: {charset_result.confidence:.3f})")
    else:
        print(f"  Charset: None")
except Exception as e:
    print(f"Confidence API error: {type(e).__name__}: {e}")