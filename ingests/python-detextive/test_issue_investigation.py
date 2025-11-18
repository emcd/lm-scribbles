#!/usr/bin/env python3
"""
Investigation script for the specific issues found in test findings.
"""

import sys
sys.path.insert(0, '/home/me/src/python-detextive/sources')

import detextive
from detextive import validation
from detextive.validation import PROFILE_TERMINAL_SAFE_ANSI, PROFILE_TEXTUAL, PROFILE_TERMINAL_SAFE

def investigate_finding_1_bom_handling():
    """Finding 1: BOM Handling Issue"""
    print("=== FINDING 1: BOM HANDLING ===")

    # Test case from findings
    content_with_bom = '\ufeffHello, world!'.encode('utf-8-sig')

    try:
        result = detextive.decode(content_with_bom)
        print(f"decode() result: {repr(result)}")
        bom_char = '\ufeff'
        print(f"BOM present in result: {result.startswith(bom_char)}")

        # Check if validation logic handles BOM properly
        text_with_bom = '\ufeffHello, world!'

        is_valid_textual = validation.is_valid_text(text_with_bom, PROFILE_TEXTUAL)
        is_valid_terminal = validation.is_valid_text(text_with_bom, PROFILE_TERMINAL_SAFE)

        print(f"Text with BOM valid in TEXTUAL profile: {is_valid_textual}")
        print(f"Text with BOM valid in TERMINAL_SAFE profile: {is_valid_terminal}")

        # Test BOM handling in validation
        print(f"PROFILE_TEXTUAL.check_bom: {PROFILE_TEXTUAL.check_bom}")
        print(f"PROFILE_TERMINAL_SAFE.check_bom: {PROFILE_TERMINAL_SAFE.check_bom}")

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

def investigate_finding_2_empty_content():
    """Finding 2: Empty Content Handling"""
    print("\n=== FINDING 2: EMPTY CONTENT ===")

    try:
        result = detextive.decode(b'')
        print(f"decode(b'') result: {repr(result)}")
        print("SUCCESS: Empty content decoded properly")
    except detextive.exceptions.ContentDecodeImpossibility:
        print("CONFIRMED BUG: Empty content raises ContentDecodeImpossibility")
    except Exception as e:
        print(f"UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()

def investigate_finding_3_escape_sequences():
    """Finding 3: Text with Escape Sequences"""
    print("\n=== FINDING 3: ESCAPE SEQUENCES ===")

    content = b'Hello\x1b[31mRed\x1b[0m'

    profiles = [
        ("TEXTUAL", PROFILE_TEXTUAL),
        ("TERMINAL_SAFE", PROFILE_TERMINAL_SAFE),
        ("TERMINAL_SAFE_ANSI", PROFILE_TERMINAL_SAFE_ANSI)
    ]

    for name, profile in profiles:
        try:
            result = detextive.decode(content, profile=profile)
            print(f"{name}: SUCCESS - {repr(result)}")
        except detextive.exceptions.TextInvalidity:
            print(f"{name}: REJECTED (validation failed)")
        except detextive.exceptions.ContentDecodeImpossibility:
            print(f"{name}: DECODE FAILED")
        except Exception as e:
            print(f"{name}: ERROR - {e}")

    # Check acceptable characters in each profile
    esc_char = '\x1b'
    print(f"\nESC character in acceptable_characters:")
    for name, profile in profiles:
        has_esc = esc_char in profile.acceptable_characters
        print(f"  {name}: {has_esc}")

def investigate_finding_4_unicode_corruption():
    """Finding 4: Unicode Symbol Corruption"""
    print("\n=== FINDING 4: UNICODE CORRUPTION ===")

    original_text = 'Unicode ★ symbols'
    content = original_text.encode('utf-8')

    try:
        decoded = detextive.decode(content)
        print(f"Original: {repr(original_text)}")
        print(f"Decoded:  {repr(decoded)}")
        print(f"Match: {original_text == decoded}")

        if original_text != decoded:
            print("CONFIRMED BUG: Unicode corruption detected")

            # Try to understand what charset was detected
            charset = detextive.detect_charset(content)
            print(f"Detected charset: {charset}")

            # Check trial decode confidence threshold
            from detextive.core import BEHAVIORS_DEFAULT
            print(f"Trial decode confidence threshold: {BEHAVIORS_DEFAULT.trial_decode_confidence}")

        else:
            print("Unicode symbols decoded correctly")

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

def investigate_finding_5_charset_inconsistency():
    """Finding 5: Charset Detection Inconsistency"""
    print("\n=== FINDING 5: CHARSET INCONSISTENCY ===")

    test_content = b'Hello, world! This is some test content.'

    # Compare different detection methods
    try:
        charset1 = detextive.detect_charset(test_content)
        charset2 = detextive.infer_charset(test_content)

        print(f"detect_charset(): {charset1}")
        print(f"infer_charset(): {charset2}")
        print(f"Match: {charset1 == charset2}")

        if charset1 != charset2:
            print("CONFIRMED: Charset detection inconsistency")

            # Try with confidence versions
            charset_conf1 = detextive.detect_charset_confidence(test_content)
            charset_conf2 = detextive.infer_charset_confidence(test_content)

            if charset_conf1:
                print(f"detect_charset_confidence(): {charset_conf1.value} (conf: {charset_conf1.confidence})")
            if charset_conf2:
                print(f"infer_charset_confidence(): {charset_conf2.value} (conf: {charset_conf2.confidence})")

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

def investigate_finding_6_default_values():
    """Finding 6: Default Values Not Working"""
    print("\n=== FINDING 6: DEFAULT VALUES ===")

    # Use problematic content that should trigger defaults
    problematic_content = b'\x01\x02\x03\x04'  # Binary-like content

    try:
        result = detextive.infer_mimetype_charset(
            problematic_content,
            mimetype_default='text/plain',
            charset_default='utf-8'
        )
        print(f"SUCCESS: {result}")

    except detextive.exceptions.MimetypeDetectFailure:
        print("CONFIRMED BUG: MimetypeDetectFailure despite defaults provided")
    except detextive.exceptions.CharsetInferFailure:
        print("CONFIRMED BUG: CharsetInferFailure despite defaults provided")
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    investigate_finding_1_bom_handling()
    investigate_finding_2_empty_content()
    investigate_finding_3_escape_sequences()
    investigate_finding_4_unicode_corruption()
    investigate_finding_5_charset_inconsistency()
    investigate_finding_6_default_values()