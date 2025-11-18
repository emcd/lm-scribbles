#!/usr/bin/env python3
"""
Analyze charset detection differences between chardet and charset-normalizer.
"""
import sys
sys.path.insert(0, 'sources')
import detextive

# Test case from documentation that changed: ISO-8859-9 → cp1250
test_content = 'Café Restaurant Menu\nEntrées: Soupe, Salade'.encode('iso-8859-1')

print("=== CHARSET DETECTION ANALYSIS ===")
print(f"Content: {test_content}")
print(f"Actual encoding: iso-8859-1")

# Test with current implementation (charset-normalizer first)
print("\n--- Current Implementation (charset-normalizer priority) ---")
try:
    charset = detextive.detect_charset(test_content)
    print(f"Detected: {charset}")

    result = detextive.detect_charset_confidence(test_content)
    print(f"With confidence: {result.charset} (conf: {result.confidence:.3f})")

    # Try decoding with detected charset
    try:
        decoded = test_content.decode(charset)
        print(f"Decoded result: {repr(decoded)}")
    except UnicodeDecodeError as e:
        print(f"Decode failed: {e}")

except Exception as e:
    print(f"Detection error: {type(e).__name__}: {e}")

# Test individual detectors
print("\n--- Individual Detector Analysis ---")

# Test chardet directly
try:
    import chardet
    chardet_result = chardet.detect(test_content)
    print(f"chardet: {chardet_result}")
except ImportError:
    print("chardet not available")

# Test charset-normalizer directly
try:
    import charset_normalizer
    cn_result = charset_normalizer.from_bytes(test_content).best()
    if cn_result:
        print(f"charset-normalizer: {cn_result.encoding}")
    else:
        print("charset-normalizer: No result")
except ImportError:
    print("charset-normalizer not available")

# Test the problematic example from advanced config
print("\n--- Advanced Config Example Analysis ---")
problematic = b'Text with\x00null bytes'
print(f"Problematic content: {problematic}")

try:
    text = detextive.decode(problematic, profile=detextive.PROFILE_TERMINAL_SAFE)
    print(f"ERROR: Should have failed but got: {repr(text)}")
except detextive.exceptions.TextInvalidity:
    print("CORRECT: TextInvalidity raised as expected")
except Exception as e:
    print(f"UNEXPECTED: {type(e).__name__}: {e}")

# Test UTF-8 with Unicode example
print("\n--- UTF-8 Unicode Example Analysis ---")
unicode_content = b'Caf\xc3\xa9 \xe2\x98\x85'
print(f"Unicode content: {unicode_content}")
print(f"Expected: 'Café ★'")

try:
    text = detextive.decode(unicode_content)
    print(f"Actual: {repr(text)}")

    charset = detextive.detect_charset(unicode_content)
    print(f"Detected charset: {charset}")

    # Try direct decode
    direct = unicode_content.decode('utf-8')
    print(f"Direct UTF-8: {repr(direct)}")

except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")