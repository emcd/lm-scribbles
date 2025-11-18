#!/usr/bin/env python3
"""
Debug why Unicode corruption persists despite trial decode being triggered.
"""

import sys
sys.path.insert(0, '/home/me/src/python-detextive/sources')

import detextive
from detextive.core import BEHAVIORS_DEFAULT
import detextive.charsets as charsets

def debug_trial_decode_process():
    """Debug the trial decode process step by step."""
    print("=== Debugging Trial Decode Process ===")

    content = 'Unicode ★ symbols'.encode('utf-8')
    print(f"Content: {content}")
    print(f"Content hex: {content.hex()}")

    # Step 1: Initial charset detection
    print("\nStep 1: Initial charset detection")
    charset_result = detextive.detect_charset_confidence(content)
    if charset_result:
        print(f"  Detected: {charset_result.value} (conf: {charset_result.confidence:.3f})")
        print(f"  Would trigger trial decode: {charset_result.confidence < BEHAVIORS_DEFAULT.trial_decode_confidence}")
    else:
        print(f"  Detection failed (None)")

    # Step 2: Check current trial_codecs
    print(f"\nStep 2: Trial decode configuration")
    print(f"  trial_codecs: {BEHAVIORS_DEFAULT.trial_codecs}")
    print(f"  trial_decode_confidence: {BEHAVIORS_DEFAULT.trial_decode_confidence}")

    # Step 3: Manual trial decode simulation
    print(f"\nStep 3: Manual trial decode simulation")
    if charset_result:
        print(f"  Starting with detected charset: {charset_result.value}")

        try:
            # Test what attempt_decodes would do
            text, decode_result = charsets.attempt_decodes(
                content,
                behaviors=BEHAVIORS_DEFAULT,
                inference=charset_result.value,
                supplement='utf-8'  # Add utf-8 as supplement
            )
            print(f"  attempt_decodes result: {repr(text)}")
            print(f"  Final charset: {decode_result.value}")
            print(f"  Final confidence: {decode_result.confidence}")

        except Exception as e:
            print(f"  attempt_decodes failed: {e}")

    # Step 4: Test individual codecs
    print(f"\nStep 4: Test individual codec decoding")
    test_codecs = ['Windows-1252', 'utf-8', 'utf-8-sig', 'iso-8859-1']

    for codec in test_codecs:
        try:
            decoded = content.decode(codec)
            original = 'Unicode ★ symbols'
            matches = decoded == original
            print(f"  {codec}: {repr(decoded)} - Matches: {matches}")
        except Exception as e:
            print(f"  {codec}: FAILED - {e}")

def debug_decode_function():
    """Debug what happens in the main decode function."""
    print("\n\n=== Debugging decode() Function ===")

    content = 'Unicode ★ symbols'.encode('utf-8')

    try:
        # Check what infer_charset_confidence returns
        print("Step 1: infer_charset_confidence")
        from detextive.core import BehaviorTristate
        import dataclasses

        # Create behaviors that disable trial decode in inference (as decode() does)
        behaviors_no_trial = dataclasses.replace(
            BEHAVIORS_DEFAULT,
            trial_decode=BehaviorTristate.Never
        )

        result = detextive.inference.infer_charset_confidence(
            content,
            behaviors=behaviors_no_trial
        )

        if result:
            print(f"  infer_charset_confidence: {result.value} (conf: {result.confidence:.3f})")

            # Step 2: What does attempt_decodes do with this?
            print("\nStep 2: attempt_decodes in decode()")
            text, final_result = charsets.attempt_decodes(
                content,
                behaviors=BEHAVIORS_DEFAULT,  # Full behaviors for final decode
                inference=result.value
            )
            print(f"  Final text: {repr(text)}")
            print(f"  Final charset: {final_result.value}")
            print(f"  Final confidence: {final_result.confidence}")
        else:
            print(f"  infer_charset_confidence: None")

    except Exception as e:
        print(f"  ERROR: {e}")
        import traceback
        traceback.print_exc()

def debug_trial_codecs_order():
    """Debug the trial codecs execution order."""
    print("\n\n=== Debugging Trial Codecs Order ===")

    content = 'Unicode ★ symbols'.encode('utf-8')

    print(f"Trial codecs: {BEHAVIORS_DEFAULT.trial_codecs}")

    # Simulate what attempt_decodes does
    print("\nSimulating attempt_decodes logic:")

    inference = 'Windows-1252'  # What chardet detected
    supplement = 'utf-8'  # What we might pass as supplement

    trial_order = []

    for codec in BEHAVIORS_DEFAULT.trial_codecs:
        if codec == detextive.core.CodecSpecifiers.FromInference:
            trial_order.append(f"FromInference -> {inference}")
        elif codec == detextive.core.CodecSpecifiers.UserDefault:
            trial_order.append(f"UserDefault -> {supplement}")
        else:
            trial_order.append(str(codec))

    print(f"Trial order: {trial_order}")

    # Test each in order
    for i, description in enumerate(trial_order):
        if '->' in description:
            _, actual_codec = description.split(' -> ')
        else:
            actual_codec = description

        try:
            decoded = content.decode(actual_codec)
            print(f"  {i+1}. {description}: SUCCESS -> {repr(decoded[:20])}")
            print(f"     This would be returned (first success wins)")
            break
        except Exception as e:
            print(f"  {i+1}. {description}: FAILED -> {e}")

def debug_charset_promotions_effect():
    """Debug how charset promotions are affecting the process."""
    print("\n\n=== Debugging Charset Promotions Effect ===")

    content = 'Unicode ★ symbols'.encode('utf-8')

    print(f"Charset promotions: {dict(BEHAVIORS_DEFAULT.charset_promotions)}")

    # What does chardet detect?
    import chardet
    raw_result = chardet.detect(content)
    print(f"Raw chardet: {raw_result}")

    detected_charset = raw_result['encoding']

    # What does promotion do?
    promoted_charset = BEHAVIORS_DEFAULT.charset_promotions.get(detected_charset, detected_charset)
    print(f"Before promotion: {detected_charset}")
    print(f"After promotion: {promoted_charset}")

    # Test both
    if detected_charset:
        try:
            decoded_original = content.decode(detected_charset)
            print(f"Original charset decode: {repr(decoded_original)}")
        except Exception as e:
            print(f"Original charset failed: {e}")

    if promoted_charset and promoted_charset != detected_charset:
        try:
            decoded_promoted = content.decode(promoted_charset)
            print(f"Promoted charset decode: {repr(decoded_promoted)}")
        except Exception as e:
            print(f"Promoted charset failed: {e}")

if __name__ == '__main__':
    debug_trial_decode_process()
    debug_decode_function()
    debug_trial_codecs_order()
    debug_charset_promotions_effect()