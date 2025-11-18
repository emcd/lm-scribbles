#!/usr/bin/env python3
"""
Test the BOM normalization fix.
"""

import sys
sys.path.insert(0, '/home/me/src/python-detextive/sources')

import detextive

def test_bom_normalization_comprehensive():
    """Comprehensive test of BOM detection normalization."""
    print("=== BOM Normalization Comprehensive Test ===")

    test_cases = [
        ("Plain UTF-8", 'Hello, world!'.encode('utf-8'), False, 'utf-8'),
        ("UTF-8-SIG encoded", 'Hello, world!'.encode('utf-8-sig'), True, 'utf-8-sig'),
        ("Manual BOM", '\ufeffHello, world!'.encode('utf-8'), True, 'utf-8-sig'),
        ("ASCII content", b'Hello world', False, 'utf-8'),
        ("UTF-8 with accents", 'Café résumé'.encode('utf-8'), False, 'utf-8'),
        ("Unicode symbols", '★ ☆ ♠ ♣'.encode('utf-8'), False, 'utf-8'),
    ]

    all_correct = True

    for name, content, has_bom, expected_charset in test_cases:
        print(f"\n{name}:")
        print(f"  Has BOM: {has_bom}")
        print(f"  Expected charset: {expected_charset}")

        # Test detection
        detected_charset = detextive.detect_charset(content)
        detected_conf = detextive.detect_charset_confidence(content)

        print(f"  Detected charset: {detected_charset}")
        if detected_conf:
            print(f"  Detected confidence: {detected_conf.value} ({detected_conf.confidence:.3f})")

        # Check accuracy
        correct = detected_charset == expected_charset
        if correct:
            print(f"  ✅ Correct detection")
        else:
            print(f"  ❌ Expected {expected_charset}, got {detected_charset}")
            all_correct = False

        # Test decode behavior
        decoded = detextive.decode(content)
        has_bom_in_text = decoded.startswith('\ufeff')

        # For BOM content, text should NOT have BOM (stripped)
        # For non-BOM content, text should NOT have BOM
        should_strip_bom = has_bom  # BOM in bytes should be stripped from text
        bom_correctly_handled = not has_bom_in_text  # Text should never have BOM

        if bom_correctly_handled:
            print(f"  ✅ BOM correctly handled in decoded text")
        else:
            print(f"  ❌ BOM handling issue: text has BOM when it shouldn't")
            all_correct = False

    return all_correct

def test_final_all_findings():
    """Final test of all findings after BOM fix."""
    print("\n=== FINAL TEST: All Findings After BOM Fix ===")

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
                print(f"  ❌ Still not matching")
                results[finding] = "FAILED"

        except Exception as e:
            print(f"  ❌ Exception: {e}")
            results[finding] = "FAILED"

    # Summary
    resolved_count = sum(1 for status in results.values() if status == "RESOLVED")
    total_count = len(results)
    print(f"\n🏆 FINAL SCORE: {resolved_count}/{total_count} findings resolved")

    return results

if __name__ == '__main__':
    normalization_correct = test_bom_normalization_comprehensive()
    findings_results = test_final_all_findings()

    print("\n" + "="*70)
    print("🎯 IMPLEMENTATION ASSESSMENT:")
    print(f"  BOM Normalization: {'✅ WORKING' if normalization_correct else '❌ ISSUES'}")
    print("  Findings Status:")
    for finding, status in findings_results.items():
        emoji = "✅" if status == "RESOLVED" else "❌"
        print(f"    {emoji} {finding}: {status}")