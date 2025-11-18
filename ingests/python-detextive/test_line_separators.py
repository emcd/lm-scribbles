#!/usr/bin/env python3
"""
Test suite for line separator functionality.
Can be adapted for pytest later.
"""

import sys
sys.path.insert(0, '/home/me/src/python-detextive/sources')

import detextive
from detextive import LineSeparators
import traceback

def test_line_separator_detection_bytes():
    """Test line separator detection from byte content."""
    print("=== Testing Line Separator Detection (Bytes) ===")
    
    test_cases = [
        ("Unix LF", b'Line 1\nLine 2\nLine 3', LineSeparators.LF),
        ("Windows CRLF", b'Line 1\r\nLine 2\r\nLine 3', LineSeparators.CRLF),
        ("Mac CR", b'Line 1\rLine 2\rLine 3', LineSeparators.CR),
        ("Mixed (LF first)", b'Line 1\nLine 2\r\nLine 3', LineSeparators.LF),
        ("Mixed (CRLF first)", b'Line 1\r\nLine 2\nLine 3', LineSeparators.CRLF),
        ("Mixed (CR first)", b'Line 1\rLine 2\nLine 3', LineSeparators.CR),
        ("No line endings", b'Single line content', None),
        ("Empty content", b'', None),
        ("Only separators", b'\n\r\n\r', LineSeparators.LF),
    ]
    
    issues = []
    
    for name, content, expected in test_cases:
        try:
            separator = LineSeparators.detect_bytes(content)
            if separator != expected:
                issues.append(f"Detection mismatch for {name}: got {separator}, expected {expected}")
            print(f"✅ {name}: {separator} (expected {expected})")
        except Exception as e:
            issues.append(f"Failed {name}: {str(e)}")
            traceback.print_exc()
            
    return issues

def test_line_separator_detection_text():
    """Test line separator detection from text strings."""
    print("\n=== Testing Line Separator Detection (Text) ===")
    
    test_cases = [
        ("Unix LF", 'Line 1\nLine 2\nLine 3', LineSeparators.LF),
        ("Windows CRLF", 'Line 1\r\nLine 2\r\nLine 3', LineSeparators.CRLF),
        ("Mac CR", 'Line 1\rLine 2\rLine 3', LineSeparators.CR),
        ("Mixed (LF first)", 'Line 1\nLine 2\r\nLine 3', LineSeparators.LF),
        ("Mixed (CRLF first)", 'Line 1\r\nLine 2\nLine 3', LineSeparators.CRLF),
        ("Mixed (CR first)", 'Line 1\rLine 2\nLine 3', LineSeparators.CR),
        ("No line endings", 'Single line content', None),
        ("Empty content", '', None),
        ("Unicode content", 'Café\nrésumé\ntest', LineSeparators.LF),
    ]
    
    issues = []
    
    for name, content, expected in test_cases:
        try:
            separator = LineSeparators.detect_text(content)
            if separator != expected:
                issues.append(f"Detection mismatch for {name}: got {separator}, expected {expected}")
            print(f"✅ {name}: {separator} (expected {expected})")
        except Exception as e:
            issues.append(f"Failed {name}: {str(e)}")
            traceback.print_exc()
            
    return issues

def test_line_separator_normalization():
    """Test universal line ending normalization."""
    print("\n=== Testing Line Separator Normalization ===")
    
    test_cases = [
        ("Unix LF", 'Line 1\nLine 2\nLine 3', 'Line 1\nLine 2\nLine 3'),
        ("Windows CRLF", 'Line 1\r\nLine 2\r\nLine 3', 'Line 1\nLine 2\nLine 3'),
        ("Mac CR", 'Line 1\rLine 2\rLine 3', 'Line 1\nLine 2\nLine 3'),
        ("Mixed endings", 'Line 1\nLine 2\r\nLine 3\rLine 4', 'Line 1\nLine 2\nLine 3\nLine 4'),
        ("No line endings", 'Single line', 'Single line'),
        ("Empty content", '', ''),
        ("Only separators", '\r\n\r\n\n', '\n\n\n'),
        ("Unicode with mixed", 'Café\r\nrésumé\ntest\r', 'Café\nrésumé\ntest\n'),
    ]
    
    issues = []
    
    for name, content, expected in test_cases:
        try:
            normalized = LineSeparators.normalize_universal(content)
            if normalized != expected:
                issues.append(f"Normalization mismatch for {name}: got {repr(normalized)}, expected {repr(expected)}")
            print(f"✅ {name}: normalized correctly")
        except Exception as e:
            issues.append(f"Failed {name}: {str(e)}")
            traceback.print_exc()
            
    return issues

def test_line_separator_nativize():
    """Test conversion to specific line ending formats."""
    print("\n=== Testing Line Separator Nativize ===")
    
    normalized_content = 'Line 1\nLine 2\nLine 3'
    
    test_cases = [
        ("LF nativize", LineSeparators.LF, 'Line 1\nLine 2\nLine 3'),
        ("CRLF nativize", LineSeparators.CRLF, 'Line 1\r\nLine 2\r\nLine 3'),
        ("CR nativize", LineSeparators.CR, 'Line 1\rLine 2\rLine 3'),
    ]
    
    issues = []
    
    for name, separator, expected in test_cases:
        try:
            result = separator.nativize(normalized_content)
            if result != expected:
                issues.append(f"Nativize mismatch for {name}: got {repr(result)}, expected {repr(expected)}")
            print(f"✅ {name}: converted correctly")
        except Exception as e:
            issues.append(f"Failed {name}: {str(e)}")
            traceback.print_exc()
            
    return issues

def test_line_separator_edge_cases():
    """Test line separator edge cases."""
    print("\n=== Testing Line Separator Edge Cases ===")
    
    issues = []
    
    edge_cases = [
        ("Very long content", 'A' * 1000 + '\n' + 'B' * 1000),
        ("Many line breaks", '\n' * 100),
        ("Alternating separators", '\n\r\n\r\n\r'),
        ("Single character", 'A'),
        ("Single newline", '\n'),
        ("Single CR", '\r'),
        ("CRLF at end", 'Content\r\n'),
        ("LF at end", 'Content\n'),
        ("No final newline", 'Line 1\nLine 2'),
    ]
    
    for name, content in edge_cases:
        try:
            # Test detection
            separator = LineSeparators.detect_text(content)
            print(f"✅ {name} detection: {separator}")
            
            # Test normalization
            normalized = LineSeparators.normalize_universal(content)
            print(f"  → Normalized: {len(normalized)} chars")
            
            # Test round-trip if separator detected
            if separator:
                converted = separator.nativize(normalized)
                print(f"  → Round-trip: {len(converted)} chars")
                
        except Exception as e:
            issues.append(f"Failed {name}: {str(e)}")
            traceback.print_exc()
            
    return issues

def test_line_separator_consistency():
    """Test consistency between detection methods."""
    print("\n=== Testing Line Separator Consistency ===")
    
    issues = []
    
    test_texts = [
        'Line 1\nLine 2\nLine 3',
        'Line 1\r\nLine 2\r\nLine 3',
        'Line 1\rLine 2\rLine 3',
        'Mixed\nLine\r\nContent\r',
        'Single line',
        '',
    ]
    
    for text in test_texts:
        try:
            # Convert to bytes and test both methods
            byte_content = text.encode('utf-8')
            
            text_result = LineSeparators.detect_text(text)
            byte_result = LineSeparators.detect_bytes(byte_content)
            
            if text_result != byte_result:
                issues.append(f"Detection inconsistency for '{repr(text)}': text={text_result}, bytes={byte_result}")
            
            print(f"✅ Consistency for {repr(text[:20])}: {text_result}")
            
        except Exception as e:
            issues.append(f"Consistency test failed for '{repr(text)}': {str(e)}")
            traceback.print_exc()
            
    return issues

def run_all_tests():
    """Run all line separator tests."""
    print("🧪 LINE SEPARATOR TEST SUITE")
    print("=" * 50)
    
    all_issues = []
    
    all_issues.extend(test_line_separator_detection_bytes())
    all_issues.extend(test_line_separator_detection_text())
    all_issues.extend(test_line_separator_normalization())
    all_issues.extend(test_line_separator_nativize())
    all_issues.extend(test_line_separator_edge_cases())
    all_issues.extend(test_line_separator_consistency())
    
    print("\n" + "=" * 50)
    print(f"LINE SEPARATOR TESTS COMPLETE")
    
    if all_issues:
        print(f"❌ Found {len(all_issues)} issues:")
        for issue in all_issues:
            print(f"  - {issue}")
        return all_issues
    else:
        print("✅ All line separator tests passed!")
        return []

if __name__ == '__main__':
    issues = run_all_tests()
    if issues:
        sys.exit(1)