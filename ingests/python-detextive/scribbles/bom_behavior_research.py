#!/usr/bin/env python3
"""
Research BOM handling behavior in Python codecs and web standards.
"""

import sys
sys.path.insert(0, '/home/me/src/python-detextive/sources')

def test_python_codec_behavior():
    """Test how Python's UTF-8 and UTF-8-sig codecs handle BOMs."""
    print("=== Python Codec BOM Behavior ===")

    original_text = "Hello, world!"

    # Encode with BOM using utf-8-sig
    with_bom = original_text.encode('utf-8-sig')
    without_bom = original_text.encode('utf-8')

    print(f"Original text: {repr(original_text)}")
    print(f"UTF-8 encoded: {repr(without_bom)}")
    print(f"UTF-8-sig encoded: {repr(with_bom)}")
    print(f"BOM bytes: {repr(with_bom[:3])}")
    print()

    # Test decoding with different codecs
    print("Decoding with different codecs:")

    # utf-8 codec with BOM content
    try:
        decoded_utf8_with_bom = with_bom.decode('utf-8')
        print(f"utf-8 decoding BOM content: {repr(decoded_utf8_with_bom)}")
        bom_char = '\ufeff'
        print(f"  BOM preserved: {decoded_utf8_with_bom.startswith(bom_char)}")
    except Exception as e:
        print(f"utf-8 decoding BOM content failed: {e}")

    # utf-8-sig codec with BOM content
    try:
        decoded_utf8sig_with_bom = with_bom.decode('utf-8-sig')
        print(f"utf-8-sig decoding BOM content: {repr(decoded_utf8sig_with_bom)}")
        bom_char = '\ufeff'
        print(f"  BOM preserved: {decoded_utf8sig_with_bom.startswith(bom_char)}")
    except Exception as e:
        print(f"utf-8-sig decoding BOM content failed: {e}")

    # utf-8 codec with non-BOM content
    try:
        decoded_utf8_without_bom = without_bom.decode('utf-8')
        print(f"utf-8 decoding non-BOM content: {repr(decoded_utf8_without_bom)}")
    except Exception as e:
        print(f"utf-8 decoding non-BOM content failed: {e}")

    # utf-8-sig codec with non-BOM content
    try:
        decoded_utf8sig_without_bom = without_bom.decode('utf-8-sig')
        print(f"utf-8-sig decoding non-BOM content: {repr(decoded_utf8sig_without_bom)}")
    except Exception as e:
        print(f"utf-8-sig decoding non-BOM content failed: {e}")

def research_web_standards():
    """Research what web standards say about BOM handling."""
    print("\n=== Web Standards Research ===")

    standards_info = [
        ("RFC 3629 (UTF-8)", "BOM is not required and should be avoided in UTF-8"),
        ("Unicode Standard", "BOM in UTF-8 is neither required nor recommended"),
        ("HTML5 Spec", "BOM should be stripped from the beginning of documents"),
        ("HTTP RFCs", "Content-Type charset parameter takes precedence over BOM"),
        ("JSON RFC 8259", "Implementations MUST NOT add BOM to JSON text"),
        ("XML Spec", "BOM may be used but is optional and can cause issues"),
    ]

    for standard, recommendation in standards_info:
        print(f"{standard}: {recommendation}")

def test_bom_in_different_contexts():
    """Test BOM behavior in various scenarios."""
    print("\n=== BOM in Different Contexts ===")

    test_cases = [
        ("Empty string with BOM", "\ufeff"),
        ("Only BOM", "\ufeff"),
        ("BOM + content", "\ufeffHello"),
        ("Content + BOM (invalid)", "Hello\ufeff"),
        ("Multiple BOMs", "\ufeff\ufeffHello"),
    ]

    for name, text in test_cases:
        print(f"\n{name}: {repr(text)}")

        # Encode and decode back
        encoded = text.encode('utf-8')
        decoded_utf8 = encoded.decode('utf-8')
        decoded_utf8sig = encoded.decode('utf-8-sig')

        print(f"  After utf-8 round-trip: {repr(decoded_utf8)}")
        print(f"  After utf-8-sig round-trip: {repr(decoded_utf8sig)}")
        print(f"  utf-8 preserves BOM: {decoded_utf8 == text}")
        bom_char = '\ufeff'
        print(f"  utf-8-sig strips leading BOM: {decoded_utf8sig != text and not decoded_utf8sig.startswith(bom_char)}")

if __name__ == '__main__':
    test_python_codec_behavior()
    research_web_standards()
    test_bom_in_different_contexts()