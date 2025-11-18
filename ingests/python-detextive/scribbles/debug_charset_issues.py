#!/usr/bin/env python3
"""
Debug specific charset detection issues.
"""
import sys
sys.path.insert(0, 'sources')
import detextive

print("=== UTF-8 CORRUPTION DEBUG ===")
utf8_content = b'Caf\xc3\xa9 \xe2\x98\x85'
print(f"Content: {utf8_content}")
print(f"Expected (direct UTF-8): {repr(utf8_content.decode('utf-8'))}")

# Test charset detection step by step
print("\n--- Charset Detection Pipeline ---")
result = detextive.detect_charset_confidence(utf8_content)
print(f"Detected: {result.charset} (conf: {result.confidence:.3f})")

# Test individual detectors
print("\n--- Individual Detectors ---")
try:
    import chardet
    chardet_result = chardet.detect(utf8_content)
    print(f"chardet: {chardet_result}")
except ImportError:
    print("chardet not available")

try:
    import charset_normalizer
    cn_result = charset_normalizer.from_bytes(utf8_content).best()
    if cn_result:
        print(f"charset-normalizer: {cn_result.encoding}")
    else:
        print("charset-normalizer: No result")
except ImportError:
    print("charset-normalizer not available")

# Test what happens during decode
print("\n--- Decode Pipeline Debug ---")
try:
    text = detextive.decode(utf8_content)
    print(f"detextive.decode result: {repr(text)}")
except Exception as e:
    print(f"decode error: {type(e).__name__}: {e}")

print("\n=== NULL BYTES DEBUG ===")
null_content = b'Text with\x00null bytes'
print(f"Content: {null_content}")

# Test charset detection
result = detextive.detect_charset_confidence(null_content)
print(f"Detected: {result.charset} (conf: {result.confidence:.3f})")

# Try decoding with detected charset
try:
    decoded = null_content.decode(result.charset)
    print(f"Decoded with {result.charset}: {repr(decoded)}")

    # Test text validation directly
    is_valid = detextive.validation.is_valid_text(decoded)
    print(f"Text validation result: {is_valid}")
    print(f"PROFILE_TEXTUAL result: {detextive.PROFILE_TEXTUAL(decoded)}")

except Exception as e:
    print(f"Decode error: {e}")

# Test individual detectors on null content
print("\n--- Individual Detectors on Null Content ---")
try:
    import chardet
    chardet_result = chardet.detect(null_content)
    print(f"chardet: {chardet_result}")
except ImportError:
    print("chardet not available")

try:
    import charset_normalizer
    cn_result = charset_normalizer.from_bytes(null_content).best()
    if cn_result:
        print(f"charset-normalizer: {cn_result.encoding}")
    else:
        print("charset-normalizer: No result")
except ImportError:
    print("charset-normalizer not available")