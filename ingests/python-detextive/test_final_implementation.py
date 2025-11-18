#!/usr/bin/env python3
"""
Test the final implementation: empty content shortcuts and BOM demotion.
"""

import sys
sys.path.insert(0, '/home/me/src/python-detextive/sources')

import detextive

def test_empty_content_shortcuts():
    """Test that all empty content shortcuts work."""
    print("=== Testing All Empty Content Shortcuts ===")

    functions_to_test = [
        ("decode", lambda: detextive.decode(b'')),
        ("detect_charset", lambda: detextive.detect_charset(b'')),
        ("detect_charset_confidence", lambda: detextive.detect_charset_confidence(b'')),
        ("infer_charset", lambda: detextive.infer_charset(b'')),
        ("infer_charset_confidence", lambda: detextive.infer_charset_confidence(b'')),
    ]

    for func_name, func_call in functions_to_test:
        print(f"\n{func_name}(b''):")
        try:
            result = func_call()
            print(f"  Result: {result}")
            print(f"  ✅ Works without exception")
        except Exception as e:
            print(f"  ❌ Exception: {e}")

def test_bom_demotion():
    """Test BOM demotion logic."""
    print("\n=== Testing BOM Demotion Logic ===")

    test_cases = [
        ("No BOM - should be utf-8", 'Hello, world!'.encode('utf-8')),
        ("With BOM - should be utf-8-sig", 'Hello, world!'.encode('utf-8-sig')),
        ("Manual BOM - should be utf-8-sig", '\ufeffHello, world!'.encode('utf-8')),
        ("UTF-8 content - should be utf-8", 'Café résumé'.encode('utf-8')),
    ]

    for name, content in test_cases:
        print(f"\n{name}:")
        bom_bytes = b'\xef\xbb\xbf'
        print(f"  Has BOM bytes: {content.startswith(bom_bytes)}")

        # What does detection return?
        charset = detextive.detect_charset(content)
        print(f"  Detected charset: {charset}")

        # What does decode return?
        decoded = detextive.decode(content)
        has_bom_in_text = decoded.startswith('\ufeff')
        print(f"  Decoded text has BOM: {has_bom_in_text}")

        # Check accuracy
        has_bom_bytes = content.startswith(b'\xef\xbb\xbf')
        should_be_sig = has_bom_bytes
        is_reported_sig = charset and 'sig' in charset.lower()

        if should_be_sig == is_reported_sig:
            print(f"  ✅ Accurate charset reporting")
        else:
            print(f"  ⚠️ Charset reporting mismatch")

def test_finding_6_supplement_behavior():
    """Test Finding 6: What happens with supplement parameters."""
    print("\n=== Testing Finding 6: Supplement Behavior ===")

    # Binary content that should fail detection
    binary_content = b'\x01\x02\x03\x04'

    print("Understanding the issue:")
    print("Current behavior: supplement is used in trial decode sequence")
    print("User expectation: supplement used as final fallback if all detection fails")
    print()

    # Test current behavior
    print("Testing infer_mimetype_charset with supplements:")
    try:
        mimetype, charset = detextive.infer_mimetype_charset(
            binary_content,
            mimetype_supplement='text/plain',
            charset_supplement='utf-8'
        )
        print(f"  SUCCESS: {mimetype}, {charset}")
        print(f"  ✅ Supplements worked as expected")
    except detextive.exceptions.MimetypeDetectFailure as e:
        print(f"  MimetypeDetectFailure: {e}")
        print(f"  ❌ Supplements not used as final fallback")
        print(f"  Issue: User expects supplements to be returned when detection fails")
    except Exception as e:
        print(f"  Other exception: {e}")

    # Show what detection actually returns for this content
    print(f"\nWhat detection returns for binary content:")
    try:
        mimetype = detextive.detect_mimetype(binary_content)
        print(f"  detect_mimetype: {mimetype}")
    except Exception as e:
        print(f"  detect_mimetype fails: {e}")

    try:
        charset = detextive.detect_charset(binary_content)
        print(f"  detect_charset: {charset}")
    except Exception as e:
        print(f"  detect_charset fails: {e}")

def test_all_original_findings():
    """Final comprehensive test of all original findings."""
    print("\n=== Final Test of All Original Findings ===")

    findings = [
        ("Finding 1: BOM handling", '\ufeffHello, world!'.encode('utf-8-sig'), 'Hello, world!'),
        ("Finding 2: Empty content", b'', ''),
        ("Finding 4: Unicode corruption", 'Unicode ★ symbols'.encode('utf-8'), 'Unicode ★ symbols'),
    ]

    results = {}

    for finding, content, expected in findings:
        print(f"\n{finding}:")
        try:
            decoded = detextive.decode(content)
            print(f"  Expected: {repr(expected)}")
            print(f"  Got:      {repr(decoded)}")

            if decoded == expected:
                print(f"  ✅ FULLY RESOLVED")
                results[finding] = "RESOLVED"
            else:
                print(f"  ⚠️ Partial: {repr(decoded)} != {repr(expected)}")
                results[finding] = "PARTIAL"

        except Exception as e:
            print(f"  ❌ Failed: {e}")
            results[finding] = "FAILED"

    # Test Finding 6 separately
    print(f"\nFinding 6: Supplement fallback behavior")
    try:
        mimetype, charset = detextive.infer_mimetype_charset(
            b'\x01\x02\x03\x04',
            mimetype_supplement='text/plain',
            charset_supplement='utf-8'
        )
        print(f"  SUCCESS: {mimetype}, {charset}")
        results["Finding 6"] = "RESOLVED"
    except Exception as e:
        print(f"  Still failing: {e}")
        results["Finding 6"] = "UNRESOLVED - needs fallback logic"

    return results

if __name__ == '__main__':
    test_empty_content_shortcuts()
    test_bom_demotion()
    test_finding_6_supplement_behavior()
    results = test_all_original_findings()

    print("\n" + "="*70)
    print("🎯 FINAL ASSESSMENT:")
    for finding, status in results.items():
        status_emoji = "✅" if status == "RESOLVED" else "⚠️" if "PARTIAL" in status else "❌"
        print(f"  {status_emoji} {finding}: {status}")

    resolved_count = sum(1 for status in results.values() if status == "RESOLVED")
    total_count = len(results)
    print(f"\n🏆 SCORE: {resolved_count}/{total_count} findings fully resolved")