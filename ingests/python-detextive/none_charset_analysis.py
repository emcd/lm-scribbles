#!/usr/bin/env python3
"""
Analyze when charset detection returns None and trial decode strategy.
"""

import sys
sys.path.insert(0, '/home/me/src/python-detextive/sources')

import detextive
from detextive.core import BEHAVIORS_DEFAULT

def analyze_none_detection_cases():
    """Find cases where charset detection returns None."""
    print("=== Cases Where Charset Detection Returns None ===")

    test_cases = [
        ("Empty content", b''),
        ("Very short binary", b'\x01'),
        ("Short binary sequence", b'\x01\x02\x03'),
        ("Mixed binary/text", b'Hello\x00\x01\x02World'),
        ("High-entropy random", bytes(range(256))),
        ("Repeated binary pattern", b'\xAA\xBB' * 100),
        ("Low-entropy binary", b'\x00' * 100),
    ]

    results = {}

    for name, content in test_cases:
        print(f"\n{name}: {repr(content[:20])}")

        try:
            # Test direct charset detection
            charset = detextive.detect_charset(content)
            charset_conf = detextive.detect_charset_confidence(content)

            print(f"  detect_charset(): {charset}")
            if charset_conf:
                print(f"  detect_charset_confidence(): {charset_conf.value} (conf: {charset_conf.confidence:.3f})")
            else:
                print(f"  detect_charset_confidence(): None")

            results[name] = {
                'charset': charset,
                'confidence': charset_conf.confidence if charset_conf else None,
                'content_length': len(content)
            }

        except Exception as e:
            print(f"  ERROR: {e}")
            results[name] = {'error': str(e)}

    return results

def test_trial_decode_strategy():
    """Test current trial decode behavior and potential improvements."""
    print("\n\n=== Current Trial Decode Strategy ===")

    # Cases where charset detection might fail but trial decode could work
    test_cases = [
        ("Valid UTF-8 but low confidence", "Héllo wörld".encode('utf-8')),
        ("ASCII that could be UTF-8", b'Hello world'),
        ("Binary that might decode", b'\x48\x65\x6c\x6c\x6f'),  # "Hello" in hex
        ("UTF-8 with some binary", "Hello\nWörld".encode('utf-8') + b'\x00'),
    ]

    print(f"Current trial_decode_confidence threshold: {BEHAVIORS_DEFAULT.trial_decode_confidence}")
    print(f"Current trial_codecs: {BEHAVIORS_DEFAULT.trial_codecs}")

    for name, content in test_cases:
        print(f"\n{name}:")
        try:
            charset_result = detextive.detect_charset_confidence(content)
            if charset_result:
                print(f"  Detected: {charset_result.value} (conf: {charset_result.confidence:.3f})")

                # Would trial decode be triggered?
                would_trial = charset_result.confidence < BEHAVIORS_DEFAULT.trial_decode_confidence
                print(f"  Would trigger trial decode: {would_trial}")

                if would_trial:
                    # Test manual trial decode
                    try:
                        decoded = content.decode('utf-8')
                        print(f"  UTF-8 decode succeeds: {repr(decoded[:50])}")
                    except UnicodeDecodeError as e:
                        print(f"  UTF-8 decode fails: {e}")

            else:
                print(f"  Detection failed (None) - trial decode should be attempted")
                # Test if manual decode would work
                for codec in ['utf-8', 'latin1', 'cp1252']:
                    try:
                        decoded = content.decode(codec)
                        print(f"  {codec} decode succeeds: {repr(decoded[:50])}")
                        break
                    except UnicodeDecodeError:
                        print(f"  {codec} decode fails")

        except Exception as e:
            print(f"  ERROR: {e}")

def analyze_mimetype_context():
    """Analyze how MIME type context affects the strategy."""
    print("\n\n=== MIME Type Context Analysis ===")

    test_content = b'\x01\x02\x03\x04'  # Binary content

    mimetype_scenarios = [
        ("No MIME type", None),
        ("Text MIME type", "text/plain"),
        ("Binary MIME type", "application/octet-stream"),
        ("JSON MIME type", "application/json"),
        ("Unknown MIME type", "application/unknown"),
    ]

    for scenario_name, mimetype in mimetype_scenarios:
        print(f"\n{scenario_name} ({mimetype}):")

        if mimetype and not mimetype.startswith('text/'):
            print("  Non-textual MIME type - should not attempt trial decode")
        else:
            print("  Textual or unknown MIME type - trial decode appropriate")

        # Test current behavior
        try:
            if mimetype:
                result = detextive.detect_charset_confidence(test_content, mimetype=mimetype)
            else:
                result = detextive.detect_charset_confidence(test_content)

            if result:
                print(f"  Detection result: {result.value} (conf: {result.confidence:.3f})")
            else:
                print(f"  Detection result: None")

        except Exception as e:
            print(f"  ERROR: {e}")

def propose_improved_strategy():
    """Propose improved strategy for handling None results."""
    print("\n\n=== Proposed Improved Strategy ===")

    strategy = """
    Current logic: charset_detection() -> None -> raise exception

    Proposed logic:
    1. charset_detection() -> result with confidence
       IF confidence >= threshold: use result
       ELSE: proceed to step 2

    2. charset_detection() -> None (no detection possible)
       IF mimetype indicates non-textual: raise appropriate exception
       ELSE: attempt trial decode with common charsets

    3. Trial decode sequence:
       - UTF-8 (most common, strict validation)
       - UTF-8 with error handling (for mixed content)
       - System default charset
       - Latin-1 (can decode any byte sequence)

    Benefits:
    - Handles borderline cases where chardet has low confidence
    - Handles cases where chardet completely fails
    - Respects MIME type hints about content type
    - Provides graceful degradation path
    """

    print(strategy)

if __name__ == '__main__':
    results = analyze_none_detection_cases()
    test_trial_decode_strategy()
    analyze_mimetype_context()
    propose_improved_strategy()