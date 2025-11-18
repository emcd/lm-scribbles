#!/usr/bin/env python3
"""
Debug the remaining issues: empty content and BOM handling.
"""

import sys
sys.path.insert(0, '/home/me/src/python-detextive/sources')

import detextive
from detextive.core import BEHAVIORS_DEFAULT

def debug_empty_content_issue():
    """Debug why empty content still fails."""
    print("=== Debugging Empty Content Issue ===")

    content = b''
    print(f"Content: {content}")

    # Check what detect_charset_confidence returns
    print("\nStep 1: detect_charset_confidence")
    try:
        result = detextive.detect_charset_confidence(content)
        print(f"  Result: {result}")
    except Exception as e:
        print(f"  Exception: {e}")

    # Check what infer_charset_confidence returns
    print("\nStep 2: infer_charset_confidence")
    try:
        result = detextive.inference.infer_charset_confidence(content)
        print(f"  Result: {result}")
    except Exception as e:
        print(f"  Exception: {e}")

    # Check if the TODO in decode() is implemented
    print("\nStep 3: decode() behavior")
    try:
        result = detextive.decode(content)
        print(f"  Success: {repr(result)}")
    except detextive.exceptions.ContentDecodeImpossibility as e:
        print(f"  ContentDecodeImpossibility: {e}")
    except Exception as e:
        print(f"  Other exception: {e}")

    # Check the TODO comment mentioned in decode()
    print("\nStep 4: Checking for empty content short-circuit in decode()")
    print("  TODO comment mentions implementing empty content handling")
    print("  This should be added at the start of decode() function")

def debug_bom_issue():
    """Debug BOM handling with charset promotions."""
    print("\n\n=== Debugging BOM Issue ===")

    # Test different BOM scenarios
    test_cases = [
        ("UTF-8-SIG encoded", '\ufeffHello, world!'.encode('utf-8-sig')),
        ("UTF-8 encoded", 'Hello, world!'.encode('utf-8')),
        ("Manual BOM + UTF-8", '\ufeffHello, world!'.encode('utf-8')),
    ]

    for name, content in test_cases:
        print(f"\n{name}:")
        print(f"  Bytes: {content}")

        # What does chardet detect?
        import chardet
        chardet_result = chardet.detect(content)
        print(f"  Chardet: {chardet_result}")

        # What does detextive detect?
        charset = detextive.detect_charset(content)
        print(f"  Detextive detect: {charset}")

        # What gets promoted?
        promoted = BEHAVIORS_DEFAULT.charset_promotions.get(charset, charset)
        print(f"  After promotion: {promoted}")

        # What does decode return?
        try:
            decoded = detextive.decode(content)
            bom_char = '\ufeff'
            has_bom = decoded.startswith(bom_char)
            print(f"  Decoded: {repr(decoded)}")
            print(f"  Has BOM: {has_bom}")
        except Exception as e:
            print(f"  Decode failed: {e}")

def debug_default_values_issue():
    """Debug why default values (supplement) still don't work."""
    print("\n\n=== Debugging Default Values Issue ===")

    content = b'\x01\x02\x03\x04'  # Binary content that should fail detection

    print(f"Content: {content}")

    # Test infer_mimetype_charset with supplements
    print("\nTesting infer_mimetype_charset with supplements:")
    try:
        mimetype, charset = detextive.infer_mimetype_charset(
            content,
            mimetype_supplement='text/plain',
            charset_supplement='utf-8'
        )
        print(f"  Success: {mimetype}, {charset}")
    except detextive.exceptions.MimetypeDetectFailure as e:
        print(f"  MimetypeDetectFailure: {e}")
        print(f"  This suggests supplement fallback logic is not implemented")
    except Exception as e:
        print(f"  Other exception: {e}")

    # Check what detection returns for this content
    print(f"\nChecking detection for binary content:")
    try:
        mimetype_result = detextive.detect_mimetype(content)
        print(f"  detect_mimetype: {mimetype_result}")
    except Exception as e:
        print(f"  detect_mimetype failed: {e}")

    try:
        charset_result = detextive.detect_charset(content)
        print(f"  detect_charset: {charset_result}")
    except Exception as e:
        print(f"  detect_charset failed: {e}")

def analyze_trial_codec_order_fix():
    """Analyze the trial codec order issue and potential fixes."""
    print("\n\n=== Analyzing Trial Codec Order Fix ===")

    print("PROBLEM IDENTIFIED:")
    print("  Current trial_codecs: (FromInference, UserDefault)")
    print("  For 'Unicode ★ symbols':")
    print("    1. FromInference = Windows-1252 -> SUCCESS (but wrong)")
    print("    2. UserDefault = utf-8 -> NEVER TRIED")
    print()
    print("SOLUTION OPTIONS:")
    print("  1. Change order to: (UserDefault, FromInference)")
    print("     - Try utf-8 first, detected charset second")
    print("  2. Add UTF-8 as explicit codec: ('utf-8', FromInference, UserDefault)")
    print("     - Always try UTF-8 first")
    print("  3. Add validation during trial decode")
    print("     - Reject results that seem incorrect")

    content = 'Unicode ★ symbols'.encode('utf-8')

    # Test what would happen with reversed order
    print(f"\nTesting reversed codec order manually:")

    # Simulate UserDefault first (utf-8)
    try:
        decoded_utf8 = content.decode('utf-8')
        print(f"  utf-8 first: {repr(decoded_utf8)} - CORRECT!")
    except Exception as e:
        print(f"  utf-8 first: FAILED - {e}")

    # Then Windows-1252
    try:
        decoded_win1252 = content.decode('Windows-1252')
        print(f"  Windows-1252 second: {repr(decoded_win1252)} - Would not be tried")
    except Exception as e:
        print(f"  Windows-1252 second: FAILED - {e}")

if __name__ == '__main__':
    debug_empty_content_issue()
    debug_bom_issue()
    debug_default_values_issue()
    analyze_trial_codec_order_fix()