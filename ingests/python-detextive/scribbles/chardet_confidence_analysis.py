#!/usr/bin/env python3
"""
Measure chardet confidence levels for Windows-1252 on Unicode content.
"""

import sys
sys.path.insert(0, '/home/me/src/python-detextive/sources')

import chardet
import detextive

def test_unicode_star_example():
    """Test the specific case from Finding 4."""
    print("=== Finding 4 Specific Case ===")

    original_text = 'Unicode ★ symbols'
    content = original_text.encode('utf-8')

    print(f"Original text: {repr(original_text)}")
    print(f"UTF-8 bytes: {content}")
    print(f"UTF-8 bytes hex: {content.hex()}")

    # Test chardet directly
    chardet_result = chardet.detect(content)
    print(f"\\nChardet raw result: {chardet_result}")

    # Test detextive detection
    charset = detextive.detect_charset(content)
    charset_conf = detextive.detect_charset_confidence(content)

    print(f"detextive detect_charset(): {charset}")
    if charset_conf:
        print(f"detextive confidence: {charset_conf.confidence}")

    # Test manual decode with detected charset
    if charset:
        try:
            decoded = content.decode(charset)
            print(f"Decoded with {charset}: {repr(decoded)}")
            print(f"Matches original: {decoded == original_text}")
        except Exception as e:
            print(f"Decode failed: {e}")

    # Test UTF-8 decode
    try:
        utf8_decoded = content.decode('utf-8')
        print(f"UTF-8 decode: {repr(utf8_decoded)}")
        print(f"UTF-8 matches original: {utf8_decoded == original_text}")
    except Exception as e:
        print(f"UTF-8 decode failed: {e}")

def test_various_unicode_content():
    """Test chardet on various Unicode content."""
    print("\\n\\n=== Various Unicode Content ===")

    test_cases = [
        ("ASCII", "Hello world"),
        ("Latin extended", "Café résumé naïve"),
        ("Unicode symbols", "★ ☆ ♠ ♣ ♥ ♦"),
        ("Mixed Unicode", "Hello ★ world café"),
        ("Emoji", "Hello 😊 world 🌟"),
        ("Cyrillic", "Привет мир"),
        ("Chinese", "你好世界"),
        ("Arabic", "مرحبا بالعالم"),
        ("Math symbols", "∑ ∫ ∞ ≤ ≥ ±"),
        ("Currency", "€ £ ¥ $ ¢"),
    ]

    results = []

    for name, text in test_cases:
        print(f"\\n{name}: {repr(text)}")
        content = text.encode('utf-8')

        # Chardet analysis
        chardet_result = chardet.detect(content)
        detected_charset = chardet_result['encoding']
        detected_confidence = chardet_result['confidence']

        print(f"  UTF-8 bytes: {content.hex()}")
        print(f"  Chardet: {detected_charset} (conf: {detected_confidence:.3f})")

        # Test decoding with detected charset
        try:
            if detected_charset:
                decoded = content.decode(detected_charset)
                matches = decoded == text
                print(f"  Decoded: {repr(decoded[:50])}")
                print(f"  Matches: {matches}")

                if not matches:
                    print(f"  *** CORRUPTION DETECTED ***")

                results.append({
                    'name': name,
                    'original': text,
                    'detected_charset': detected_charset,
                    'confidence': detected_confidence,
                    'corrupted': not matches
                })
        except Exception as e:
            print(f"  Decode error: {e}")
            results.append({
                'name': name,
                'original': text,
                'detected_charset': detected_charset,
                'confidence': detected_confidence,
                'decode_error': str(e)
            })

    return results

def analyze_confidence_thresholds():
    """Analyze what confidence thresholds would prevent corruption."""
    print("\\n\\n=== Confidence Threshold Analysis ===")

    # Test cases known to cause issues
    problematic_cases = [
        'Unicode ★ symbols',
        'Café résumé ★ naïve',
        'Hello ♠ ♣ ♥ ♦ world',
        '€ £ ¥ symbols',
    ]

    print("Analyzing confidence levels for problematic cases:")

    for text in problematic_cases:
        content = text.encode('utf-8')
        chardet_result = chardet.detect(content)

        charset = chardet_result['encoding']
        confidence = chardet_result['confidence']

        print(f"\\n{repr(text)}")
        print(f"  Chardet: {charset} (conf: {confidence:.3f})")

        if charset and charset != 'utf-8':
            print(f"  *** Would cause corruption at threshold {confidence:.3f} ***")

        # Check at different thresholds
        thresholds = [0.5, 0.6, 0.7, 0.8, 0.9]
        for threshold in thresholds:
            would_trigger_trial = confidence < threshold
            print(f"  At threshold {threshold}: trial decode = {would_trigger_trial}")

def test_chardet_patterns():
    """Test patterns that confuse chardet."""
    print("\\n\\n=== Chardet Confusion Patterns ===")

    # Patterns that might trigger Windows-1252 detection
    test_patterns = [
        ("Single Unicode char", "★"),
        ("Double Unicode char", "★★"),
        ("Unicode in context", "A★B"),
        ("Multiple Unicode", "★☆♠♣"),
        ("Unicode + Latin", "café★résumé"),
        ("Short Unicode text", "★ symbol"),
        ("Medium Unicode text", "Unicode ★ symbols are cool"),
    ]

    for name, text in test_patterns:
        content = text.encode('utf-8')
        chardet_result = chardet.detect(content)

        print(f"\\n{name}: {repr(text)}")
        print(f"  Length: {len(content)} bytes")
        print(f"  Chardet: {chardet_result['encoding']} (conf: {chardet_result['confidence']:.3f})")

        # Analyze byte patterns
        print(f"  Bytes: {content.hex()}")

        # Check if specific byte sequences trigger Windows-1252
        if chardet_result['encoding'] in ['windows-1252', 'Windows-1252']:
            print(f"  *** TRIGGERS WINDOWS-1252 ***")

if __name__ == '__main__':
    test_unicode_star_example()
    results = test_various_unicode_content()
    analyze_confidence_thresholds()
    test_chardet_patterns()

    # Summary
    print("\\n\\n=== SUMMARY ===")
    corrupted_count = sum(1 for r in results if r.get('corrupted', False))
    total_count = len(results)
    print(f"Corrupted results: {corrupted_count}/{total_count}")

    if corrupted_count > 0:
        print("\\nCorrupted cases:")
        for result in results:
            if result.get('corrupted'):
                print(f"  {result['name']}: {result['detected_charset']} (conf: {result['confidence']:.3f})")