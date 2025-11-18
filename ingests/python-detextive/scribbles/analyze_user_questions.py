#!/usr/bin/env python3
"""
Analyze the user's specific questions about UTF-8 inference, BOM handling, and confidence values.
"""

import sys
sys.path.insert(0, '/home/me/src/python-detextive/sources')

import detextive
from detextive.core import BEHAVIORS_DEFAULT

def analyze_utf8_as_inference():
    """Analyze sending utf-8 as inference charset for problematic cases."""
    print("=== UTF-8 as Inference Charset Analysis ===")

    content = 'Unicode ★ symbols'.encode('utf-8')

    print("Current flow:")
    print("  chardet detects: Windows-1252 (0.730)")
    print("  trial_codecs: (FromInference, UserDefault)")
    print("  Result: Windows-1252 succeeds, utf-8 never tried")
    print()

    print("Proposed approach: Force UTF-8 as inference for suspicious cases")
    print("Benefits:")
    print("  - More targeted than changing global trial codec order")
    print("  - Could detect Windows-1252 on UTF-8 content pattern")
    print("  - Preserves existing logic for legitimate cases")
    print()

    # Test what this would look like
    print("Implementation ideas:")
    print("1. In charset promotions:")
    print("   - Add promotion: 'Windows-1252' → 'utf-8' (when confidence < 0.8)")
    print("   - Problem: Too broad, would affect legitimate Windows-1252")
    print()
    print("2. In detection confirmation logic:")
    print("   - Check if Windows-1252 result can also decode as UTF-8")
    print("   - If yes, prefer UTF-8")
    print("   - More precise targeting")
    print()
    print("3. Modify inference logic:")
    print("   - When charset detection gives Windows-1252 with low confidence")
    print("   - Override inference to 'utf-8' for trial decode")

def analyze_bom_handling_correctness():
    """Analyze if the utf-8 → utf-8-sig promotion correctly handles BOMs."""
    print("\\n\\n=== BOM Handling Analysis ===")

    print("Current promotion: {'utf-8': 'utf-8-sig'}")
    print()

    # Test various BOM scenarios properly
    test_cases = [
        ("Plain UTF-8", 'Hello, world!'.encode('utf-8')),
        ("UTF-8 with manual BOM", ('\\ufeff' + 'Hello, world!').encode('utf-8')),
        ("UTF-8-SIG encoded", 'Hello, world!'.encode('utf-8-sig')),
        ("Double BOM issue", ('\\ufeff' + 'Hello, world!').encode('utf-8-sig')),
    ]

    for name, content in test_cases:
        print(f"\\n{name}:")
        print(f"  Bytes: {content.hex()}")

        # What does chardet see?
        import chardet
        detected = chardet.detect(content)['encoding']
        print(f"  Chardet: {detected}")

        # What does promotion do?
        promoted = BEHAVIORS_DEFAULT.charset_promotions.get(detected, detected) if detected else None
        print(f"  Promoted: {promoted}")

        # Test manual decoding
        if promoted:
            try:
                decoded = content.decode(promoted)
                bom_char = '\\ufeff'
                has_bom = decoded.startswith(bom_char)
                print(f"  Manual decode: {repr(decoded)}")
                print(f"  BOM stripped: {not has_bom}")
            except Exception as e:
                print(f"  Decode failed: {e}")

def analyze_confidence_values():
    """Analyze typical confidence values to recommend threshold."""
    print("\\n\\n=== Confidence Values Analysis ===")

    test_cases = [
        ("Perfect ASCII", b'Hello world'),
        ("Clean UTF-8", 'Café résumé'.encode('utf-8')),
        ("Unicode symbols", '★ ☆ ♠ ♣ ♥ ♦'.encode('utf-8')),
        ("Mixed content", 'Hello ★ world café'.encode('utf-8')),
        ("Cyrillic", 'Привет мир'.encode('utf-8')),
        ("Chinese", '你好世界'.encode('utf-8')),
        ("Math symbols", '∑ ∫ ∞ ≤ ≥ ±'.encode('utf-8')),
        ("Problematic case", 'Unicode ★ symbols'.encode('utf-8')),
        ("Short Unicode", '★'.encode('utf-8')),
        ("Binary-like", bytes([0x80, 0x81, 0x82, 0x83])),
    ]

    confidence_ranges = {
        "perfect": [],
        "high": [],      # 0.9-0.99
        "medium": [],    # 0.7-0.89
        "low": [],       # 0.5-0.69
        "very_low": []   # <0.5
    }

    print("Confidence distribution:")

    for name, content in test_cases:
        try:
            result = detextive.detect_charset_confidence(content)
            if result:
                conf = result.confidence
                charset = result.value

                # Categorize
                if conf == 1.0:
                    confidence_ranges["perfect"].append((name, charset, conf))
                elif conf >= 0.9:
                    confidence_ranges["high"].append((name, charset, conf))
                elif conf >= 0.7:
                    confidence_ranges["medium"].append((name, charset, conf))
                elif conf >= 0.5:
                    confidence_ranges["low"].append((name, charset, conf))
                else:
                    confidence_ranges["very_low"].append((name, charset, conf))

                print(f"  {name:20s}: {charset:12s} ({conf:.3f})")
            else:
                print(f"  {name:20s}: None")
        except Exception as e:
            print(f"  {name:20s}: ERROR - {e}")

    print("\\nConfidence Range Analysis:")
    for range_name, cases in confidence_ranges.items():
        if cases:
            print(f"\\n{range_name.upper()} ({len(cases)} cases):")
            for name, charset, conf in cases:
                print(f"  {name}: {charset} ({conf:.3f})")

    print("\\nThreshold Recommendations:")
    print("  0.95: Would trigger trial decode for almost everything (too aggressive)")
    print("  0.90: Would trigger for medium confidence cases (reasonable)")
    print("  0.80: Would trigger for problematic cases + some medium (balanced)")
    print("  0.70: Would only trigger for clearly problematic cases (conservative)")

    # Count how many would trigger at each threshold
    all_confidences = []
    for range_cases in confidence_ranges.values():
        all_confidences.extend([conf for _, _, conf in range_cases])

    thresholds = [0.95, 0.90, 0.80, 0.70]
    print("\\nTrial decode trigger rates:")
    for threshold in thresholds:
        trigger_count = sum(1 for conf in all_confidences if conf < threshold)
        total = len(all_confidences)
        rate = trigger_count / total * 100 if total > 0 else 0
        print(f"  {threshold}: {trigger_count}/{total} cases ({rate:.1f}%)")

if __name__ == '__main__':
    analyze_utf8_as_inference()
    analyze_bom_handling_correctness()
    analyze_confidence_values()