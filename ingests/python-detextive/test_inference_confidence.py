#!/usr/bin/env python3
"""
Test the new infer_mimetype_charset_confidence implementation.
"""

import sys
sys.path.insert(0, '/home/me/src/python-detextive/sources')

import detextive

def test_inference_confidence_api():
    """Test the new confidence-based inference API."""
    print("=== Testing infer_mimetype_charset_confidence API ===")

    test_cases = [
        ("JSON content", b'{"hello": "world"}'),
        ("Plain text", b'Hello, world!'),
        ("Unicode text", 'Unicode ★ symbols'.encode('utf-8')),
        ("Empty content", b''),
        ("Binary content", b'\x01\x02\x03\x04'),
    ]

    for name, content in test_cases:
        print(f"\n{name}:")
        try:
            # Test new confidence API
            mimetype_result, charset_result = detextive.infer_mimetype_charset_confidence(content)

            print(f"  Mimetype: {mimetype_result.value} (conf: {mimetype_result.confidence:.3f})")
            if charset_result:
                print(f"  Charset: {charset_result.value} (conf: {charset_result.confidence:.3f})")
            else:
                print(f"  Charset: None")

            # Test old API still works
            mimetype, charset = detextive.infer_mimetype_charset(content)
            print(f"  Old API: {mimetype}, {charset}")

        except Exception as e:
            print(f"  ERROR: {e}")

def test_decode_with_confidence():
    """Test decode using the new confidence-based logic."""
    print("\n=== Testing decode with confidence logic ===")

    test_cases = [
        ("Empty content", b''),
        ("Unicode corruption case", 'Unicode ★ symbols'.encode('utf-8')),
        ("Binary that might be textual", b'\x48\x65\x6c\x6c\x6f'),  # "Hello" in bytes
        ("Clearly binary", b'\x00\x01\x02\x03'),
    ]

    for name, content in test_cases:
        print(f"\n{name}:")
        try:
            decoded = detextive.decode(content)
            print(f"  SUCCESS: {repr(decoded[:50])}")
        except detextive.exceptions.ContentDecodeImpossibility:
            print(f"  ContentDecodeImpossibility (expected for binary)")
        except Exception as e:
            print(f"  ERROR: {e}")

def test_utf8_trial_decode_problem():
    """Test the UTF-8 trial decode problem the user identified."""
    print("\n=== Testing UTF-8 Trial Decode Problem ===")

    problematic_cases = [
        b'\x00\x01\x02',
        b'\x00' * 100,
        b'\xff\xfe\xfd',
        b'\x80\x81\x82\x83',
    ]

    for content in problematic_cases:
        print(f"\nContent: {content.hex()[:20]}...")

        # Can it decode as UTF-8?
        try:
            decoded = content.decode('utf-8-sig')
            print(f"  UTF-8-SIG decode: SUCCESS -> {repr(decoded[:20])}")
            print(f"  This is clearly not text but UTF-8 accepts it!")

            # Would PROFILE_TEXTUAL catch it?
            is_valid = detextive.validation.is_valid_text(decoded)
            print(f"  PROFILE_TEXTUAL validation: {'PASS' if is_valid else 'REJECT'}")

        except UnicodeDecodeError:
            print(f"  UTF-8-SIG decode: FAILED (good)")

if __name__ == '__main__':
    test_inference_confidence_api()
    test_decode_with_confidence()
    test_utf8_trial_decode_problem()