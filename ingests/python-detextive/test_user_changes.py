#!/usr/bin/env python3
"""
Test the user's changes to see if they resolve the reported issues.
"""

import sys
sys.path.insert(0, '/home/me/src/python-detextive/sources')

import detextive
from detextive.core import BEHAVIORS_DEFAULT

def test_confidence_threshold_impact():
    """Test impact of new 0.95 confidence thresholds."""
    print("=== Testing New Confidence Thresholds (0.95) ===")

    print(f"New trial_decode_confidence: {BEHAVIORS_DEFAULT.trial_decode_confidence}")
    print(f"New text_validate_confidence: {BEHAVIORS_DEFAULT.text_validate_confidence}")

    # Test cases that had various confidence levels
    test_cases = [
        ("Unicode corruption case", 'Unicode ★ symbols'.encode('utf-8')),
        ("Valid UTF-8 medium conf", 'Hello ★ world café'.encode('utf-8')),  # Was 0.752
        ("Latin extended", 'Café résumé naïve'.encode('utf-8')),  # Was 0.938
        ("ASCII content", b'Hello world'),  # Was 1.000
        ("Short Unicode", '★'.encode('utf-8')),  # Was Windows-1252 0.730
    ]

    for name, content in test_cases:
        print(f"\n{name}:")
        try:
            # Check charset detection confidence
            charset_conf = detextive.detect_charset_confidence(content)
            if charset_conf:
                print(f"  Detected: {charset_conf.value} (conf: {charset_conf.confidence:.3f})")

                # Would this trigger trial decode now?
                would_trigger_trial = charset_conf.confidence < BEHAVIORS_DEFAULT.trial_decode_confidence
                would_trigger_validation = charset_conf.confidence < BEHAVIORS_DEFAULT.text_validate_confidence

                print(f"  Would trigger trial decode: {would_trigger_trial}")
                print(f"  Would trigger validation: {would_trigger_validation}")

                # Test actual decode to see behavior
                decoded = detextive.decode(content)
                print(f"  Decode result: {repr(decoded[:30])}")

            else:
                print(f"  Detection failed (None)")

        except Exception as e:
            print(f"  ERROR: {e}")

def test_charset_promotions():
    """Test new charset promotions to utf-8-sig."""
    print("\n\n=== Testing Charset Promotions ===")

    print(f"Charset promotions: {dict(BEHAVIORS_DEFAULT.charset_promotions)}")

    # Test BOM handling with promotions
    bom_cases = [
        ("UTF-8 with BOM", '\ufeffHello, world!'.encode('utf-8-sig')),
        ("UTF-8 without BOM", 'Hello, world!'.encode('utf-8')),
        ("ASCII content", b'Hello world'),
    ]

    for name, content in bom_cases:
        print(f"\n{name}:")
        try:
            # Check what gets detected
            charset = detextive.detect_charset(content)
            print(f"  Detected charset: {charset}")

            # Test decode
            decoded = detextive.decode(content)
            bom_char = '\ufeff'
            has_bom = decoded.startswith(bom_char)
            print(f"  Decoded: {repr(decoded)}")
            print(f"  Has BOM: {has_bom}")

            if name == "UTF-8 with BOM" and has_bom:
                print(f"  *** BOM NOT STRIPPED - Issue may persist ***")
            elif name == "UTF-8 with BOM" and not has_bom:
                print(f"  ✅ BOM correctly stripped by charset promotion")

        except Exception as e:
            print(f"  ERROR: {e}")

def test_trial_decode_logic():
    """Test trial_decode_as_necessary vs trial_decode_as_confident."""
    print("\n\n=== Testing Trial Decode Logic ===")

    # Test case where charset detection returns None
    empty_content = b''

    print("Testing empty content (charset detection returns None):")
    try:
        charset_conf = detextive.detect_charset_confidence(empty_content)
        print(f"  detect_charset_confidence: {charset_conf}")

        # This should trigger the new trial_decode_as_necessary logic
        # if mimetype is textual
        try:
            decoded = detextive.decode(empty_content)
            print(f"  decode() succeeded: {repr(decoded)}")
        except detextive.exceptions.ContentDecodeImpossibility:
            print(f"  decode() still fails with ContentDecodeImpossibility")
        except Exception as e:
            print(f"  decode() failed with: {e}")

    except Exception as e:
        print(f"  ERROR in detection: {e}")

def test_supplement_parameters():
    """Test that supplement parameter renaming works."""
    print("\n\n=== Testing Supplement Parameters ===")

    content = b'Hello world'

    try:
        # Test charset_supplement
        result = detextive.infer_charset(
            content,
            charset_supplement='iso-8859-1'
        )
        print(f"infer_charset with charset_supplement: {result}")

        # Test mimetype_supplement
        result2 = detextive.infer_charset(
            content,
            mimetype_supplement='text/plain'
        )
        print(f"infer_charset with mimetype_supplement: {result2}")

        # Test decode with charset_supplement
        result3 = detextive.decode(
            content,
            charset_supplement='utf-8'
        )
        print(f"decode with charset_supplement: {repr(result3)}")

        print("✅ Supplement parameters working correctly")

    except Exception as e:
        print(f"ERROR with supplement parameters: {e}")
        import traceback
        traceback.print_exc()

def test_original_failing_cases():
    """Retest the original failing cases from the findings."""
    print("\n\n=== Retesting Original Failing Cases ===")

    original_cases = [
        ("Finding 1: BOM handling", '\ufeffHello, world!'.encode('utf-8-sig'), 'Hello, world!'),
        ("Finding 2: Empty content", b'', ''),
        ("Finding 4: Unicode corruption", 'Unicode ★ symbols'.encode('utf-8'), 'Unicode ★ symbols'),
        ("Finding 6: Default values", b'\x01\x02\x03\x04', None),  # Special case
    ]

    results = {}

    for name, content, expected in original_cases:
        print(f"\n{name}:")

        if name == "Finding 6: Default values":
            # Test with supplement values
            try:
                mimetype, charset = detextive.infer_mimetype_charset(
                    content,
                    mimetype_supplement='text/plain',
                    charset_supplement='utf-8'
                )
                print(f"  SUCCESS: {mimetype}, {charset}")
                results[name] = "RESOLVED"
            except Exception as e:
                print(f"  STILL FAILING: {e}")
                results[name] = "UNRESOLVED"
        else:
            # Standard decode test
            try:
                decoded = detextive.decode(content)
                print(f"  Decoded: {repr(decoded)}")

                if decoded == expected:
                    print(f"  ✅ RESOLVED: Matches expected output")
                    results[name] = "RESOLVED"
                else:
                    print(f"  ❌ PARTIALLY RESOLVED: Got {repr(decoded)}, expected {repr(expected)}")
                    results[name] = "PARTIALLY RESOLVED"

            except Exception as e:
                print(f"  ❌ STILL FAILING: {e}")
                results[name] = "UNRESOLVED"

    return results

if __name__ == '__main__':
    test_confidence_threshold_impact()
    test_charset_promotions()
    test_trial_decode_logic()
    test_supplement_parameters()
    results = test_original_failing_cases()

    print("\n" + "="*60)
    print("SUMMARY OF ORIGINAL ISSUES:")
    for finding, status in results.items():
        print(f"  {finding}: {status}")