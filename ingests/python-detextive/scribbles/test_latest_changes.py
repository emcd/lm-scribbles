#!/usr/bin/env python3
"""
Test the latest user changes: empty content, utf-8-sig inference, and 0.8 thresholds.
"""

import sys
sys.path.insert(0, '/home/me/src/python-detextive/sources')

import detextive
from detextive.core import BEHAVIORS_DEFAULT

def test_empty_content_fix():
    """Test that empty content short-circuit works."""
    print("=== Testing Empty Content Fix ===")

    try:
        result = detextive.decode(b'')
        print(f"decode(b'') result: {repr(result)}")
        if result == '':
            print("✅ Empty content fix WORKING")
        else:
            print(f"❌ Expected '', got {repr(result)}")
    except Exception as e:
        print(f"❌ Empty content still failing: {e}")

def test_unicode_corruption_fix():
    """Test if the utf-8-sig inference fixes Unicode corruption."""
    print("\n=== Testing Unicode Corruption Fix ===")

    test_cases = [
        ("Original problem case", 'Unicode ★ symbols'.encode('utf-8')),
        ("Short Unicode", '★'.encode('utf-8')),
        ("Mixed Unicode Latin", 'Hello ★ world café'.encode('utf-8')),
    ]

    for name, content in test_cases:
        print(f"\n{name}:")
        try:
            # Check detection first
            charset_conf = detextive.detect_charset_confidence(content)
            if charset_conf:
                print(f"  Detection: {charset_conf.value} (conf: {charset_conf.confidence:.3f})")
                print(f"  Would trigger trial: {charset_conf.confidence < BEHAVIORS_DEFAULT.trial_decode_confidence}")

            # Test decode
            decoded = detextive.decode(content)
            original = content.decode('utf-8')  # What it should be
            matches = decoded == original

            print(f"  Expected: {repr(original)}")
            print(f"  Got:      {repr(decoded)}")
            print(f"  ✅ FIXED" if matches else "❌ STILL CORRUPTED")

        except Exception as e:
            print(f"  ERROR: {e}")

def test_bom_detection_accuracy():
    """Test BOM detection and whether utf-8-sig reporting is accurate."""
    print("\n=== Testing BOM Detection Accuracy ===")

    test_cases = [
        ("No BOM", 'Hello, world!'.encode('utf-8')),
        ("With BOM", 'Hello, world!'.encode('utf-8-sig')),
        ("Manual BOM in string", '\ufeffHello, world!'.encode('utf-8')),
        ("UTF-8 content", 'Café résumé'.encode('utf-8')),
    ]

    for name, content in test_cases:
        print(f"\n{name}:")
        print(f"  Bytes: {content.hex()}")

        # Check if BOM is actually present in bytes
        has_bom_bytes = content.startswith(b'\xef\xbb\xbf')
        print(f"  Has BOM in bytes: {has_bom_bytes}")

        # What does detextive detect?
        charset = detextive.detect_charset(content)
        print(f"  Detected charset: {charset}")

        # Is the detection accurate?
        should_be_utf8sig = has_bom_bytes
        is_reported_utf8sig = charset and 'sig' in charset.lower()

        if should_be_utf8sig == is_reported_utf8sig:
            print(f"  ✅ Accurate reporting")
        else:
            if should_be_utf8sig and not is_reported_utf8sig:
                print(f"  ⚠️ Has BOM but reported as {charset}")
            else:
                print(f"  ⚠️ No BOM but reported as {charset}")
                print(f"  This suggests need for BOM check and demotion")

def test_confidence_threshold_impact():
    """Test impact of 0.8 confidence thresholds."""
    print("\n=== Testing 0.8 Confidence Thresholds ===")

    print(f"New thresholds: trial_decode={BEHAVIORS_DEFAULT.trial_decode_confidence}, text_validate={BEHAVIORS_DEFAULT.text_validate_confidence}")

    test_cases = [
        ("High confidence", 'Hello world'.encode('utf-8')),  # Usually 1.0
        ("Medium confidence", '★ ☆ ♠ ♣'.encode('utf-8')),   # Usually 0.99
        ("Problem case", 'Unicode ★ symbols'.encode('utf-8')),  # Usually 0.73
        ("Very low confidence", 'Café résumé naïve'.encode('utf-8')),  # Can be very low
    ]

    for name, content in test_cases:
        print(f"\n{name}:")
        try:
            charset_conf = detextive.detect_charset_confidence(content)
            if charset_conf:
                print(f"  Confidence: {charset_conf.confidence:.3f}")
                print(f"  Would trigger trial: {charset_conf.confidence < BEHAVIORS_DEFAULT.trial_decode_confidence}")
                print(f"  Would validate: {charset_conf.confidence < BEHAVIORS_DEFAULT.text_validate_confidence}")
            else:
                print(f"  Detection failed (None)")
        except Exception as e:
            print(f"  ERROR: {e}")

def check_other_functions_needing_shortcuts():
    """Check if other functions still need empty content shortcuts."""
    print("\n=== Checking Other Functions for Empty Content ===")

    content = b''

    functions_to_test = [
        ("detect_charset", lambda: detextive.detect_charset(content)),
        ("detect_charset_confidence", lambda: detextive.detect_charset_confidence(content)),
        ("infer_charset", lambda: detextive.infer_charset(content)),
        ("infer_charset_confidence", lambda: detextive.infer_charset_confidence(content)),
    ]

    for func_name, func_call in functions_to_test:
        print(f"\n{func_name}(b''):")
        try:
            result = func_call()
            print(f"  Result: {result}")
            if result is None:
                print(f"  ⚠️ Returns None - might benefit from shortcut returning sensible default")
        except Exception as e:
            print(f"  Exception: {e}")
            print(f"  ⚠️ Might need empty content shortcut")

def test_original_failing_cases_final():
    """Final test of all original failing cases."""
    print("\n=== Final Test of Original Issues ===")

    test_cases = [
        ("Finding 1: BOM", '\ufeffHello, world!'.encode('utf-8-sig'), 'Hello, world!'),
        ("Finding 2: Empty", b'', ''),
        ("Finding 4: Unicode corruption", 'Unicode ★ symbols'.encode('utf-8'), 'Unicode ★ symbols'),
    ]

    results = {}

    for name, content, expected in test_cases:
        print(f"\n{name}:")
        try:
            decoded = detextive.decode(content)
            print(f"  Expected: {repr(expected)}")
            print(f"  Got:      {repr(decoded)}")

            if decoded == expected:
                print(f"  ✅ FULLY RESOLVED")
                results[name] = "RESOLVED"
            else:
                print(f"  ⚠️ Still not matching exactly")
                results[name] = "PARTIAL"

        except Exception as e:
            print(f"  ❌ Still failing: {e}")
            results[name] = "FAILED"

    return results

if __name__ == '__main__':
    test_empty_content_fix()
    test_unicode_corruption_fix()
    test_bom_detection_accuracy()
    test_confidence_threshold_impact()
    check_other_functions_needing_shortcuts()
    results = test_original_failing_cases_final()

    print("\n" + "="*60)
    print("FINAL SUMMARY:")
    for issue, status in results.items():
        print(f"  {issue}: {status}")