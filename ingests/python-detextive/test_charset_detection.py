#!/usr/bin/env python3
"""
Test suite for charset detection functionality.
Can be adapted for pytest later.
"""

import sys
sys.path.insert(0, '/home/me/src/python-detextive/sources')

import detextive
from detextive import Behaviors, BehaviorTristate
import traceback

def test_basic_charset_detection():
    """Test basic charset detection with common encodings."""
    print("=== Testing Basic Charset Detection ===")
    
    test_cases = [
        ("UTF-8 with BOM", '\ufeffHello, world!'.encode('utf-8-sig')),
        ("UTF-8 without BOM", 'Hello, world!'.encode('utf-8')),
        ("ASCII content", 'Hello world'.encode('ascii')),
        ("UTF-8 with unicode", 'Café ★ résumé'.encode('utf-8')),
        ("ISO-8859-1", 'Café Restaurant Menu\nEntrées: Soupe, Salade'.encode('iso-8859-1')),
        ("Windows-1252", 'Smart "quotes" and –dashes—'.encode('windows-1252', errors='ignore')),
    ]
    
    issues = []
    
    for name, content in test_cases:
        try:
            charset = detextive.detect_charset(content)
            result = detextive.detect_charset_confidence(content)
            print(f"✅ {name}: {charset} (confidence: {result.confidence:.3f})")
            
            # Test that confidence function returns same charset
            if result.value != charset:
                issues.append(f"Charset mismatch: detect_charset='{charset}' vs detect_charset_confidence='{result.value}'")
                
        except Exception as e:
            issues.append(f"Failed {name}: {str(e)}")
            print(f"❌ {name}: {str(e)}")
            
    return issues

def test_charset_edge_cases():
    """Test charset detection edge cases."""
    print("\n=== Testing Charset Edge Cases ===")
    
    issues = []
    
    # Empty content
    try:
        result = detextive.detect_charset(b'')
        if result is not None:
            issues.append(f"Empty content should return None, got: {result}")
        else:
            print("✅ Empty content: None")
    except Exception as e:
        issues.append(f"Empty content failed: {str(e)}")
        
    # Very short content
    try:
        result = detextive.detect_charset(b'a')
        print(f"✅ Single byte: {result}")
    except Exception as e:
        issues.append(f"Single byte failed: {str(e)}")
        
    # Binary content
    try:
        result = detextive.detect_charset(b'\x00\x01\x02\x03\xff\xfe\xfd')
        print(f"✅ Binary content: {result}")
    except Exception as e:
        issues.append(f"Binary content failed: {str(e)}")
        
    # Very long content
    try:
        long_content = ('Hello world! ' * 1000).encode('utf-8')
        result = detextive.detect_charset(long_content)
        confidence = detextive.detect_charset_confidence(long_content)
        print(f"✅ Long content: {result} (confidence: {confidence.confidence:.3f})")
    except Exception as e:
        issues.append(f"Long content failed: {str(e)}")
        
    return issues

def test_charset_with_behaviors():
    """Test charset detection with custom behaviors."""
    print("\n=== Testing Charset with Custom Behaviors ===")
    
    issues = []
    content = 'Test content for behaviors'.encode('utf-8')
    
    try:
        # Test with custom confidence divisor
        custom_behaviors = Behaviors(
            bytes_quantity_confidence_divisor=128,
            trial_decode=BehaviorTristate.Always
        )
        
        result1 = detextive.detect_charset_confidence(content)
        result2 = detextive.detect_charset_confidence(content, behaviors=custom_behaviors)
        
        print(f"✅ Default behaviors: {result1.value} (confidence: {result1.confidence:.3f})")
        print(f"✅ Custom behaviors: {result2.value} (confidence: {result2.confidence:.3f})")
        
        # Custom behaviors should potentially change confidence
        if result1.confidence == result2.confidence:
            print("⚠️  Custom behaviors didn't change confidence (may be expected)")
            
    except Exception as e:
        issues.append(f"Custom behaviors failed: {str(e)}")
        traceback.print_exc()
        
    return issues

def test_charset_with_mimetype_hint():
    """Test charset detection with MIME type hints."""
    print("\n=== Testing Charset with MIME Type Hints ===")
    
    issues = []
    content = b'{"key": "value"}'
    
    try:
        # Without MIME type
        charset1 = detextive.detect_charset(content)
        
        # With MIME type hint
        charset2 = detextive.detect_charset(content, mimetype='application/json')
        
        print(f"✅ Without MIME hint: {charset1}")
        print(f"✅ With MIME hint: {charset2}")
        
    except Exception as e:
        issues.append(f"MIME type hint test failed: {str(e)}")
        traceback.print_exc()
        
    return issues

def test_charset_with_location():
    """Test charset detection with location parameter."""
    print("\n=== Testing Charset with Location ===")
    
    issues = []
    content = b'Sample content'
    
    try:
        # Test various location types
        locations = [
            'file.txt',
            'path/to/file.json',
            '/absolute/path/file.py',
            None
        ]
        
        for location in locations:
            charset = detextive.detect_charset(content, location=location)
            print(f"✅ Location '{location}': {charset}")
            
    except Exception as e:
        issues.append(f"Location test failed: {str(e)}")
        traceback.print_exc()
        
    return issues

def run_all_tests():
    """Run all charset detection tests."""
    print("🧪 CHARSET DETECTION TEST SUITE")
    print("=" * 50)
    
    all_issues = []
    
    all_issues.extend(test_basic_charset_detection())
    all_issues.extend(test_charset_edge_cases())
    all_issues.extend(test_charset_with_behaviors())
    all_issues.extend(test_charset_with_mimetype_hint())
    all_issues.extend(test_charset_with_location())
    
    print("\n" + "=" * 50)
    print(f"CHARSET TESTS COMPLETE")
    
    if all_issues:
        print(f"❌ Found {len(all_issues)} issues:")
        for issue in all_issues:
            print(f"  - {issue}")
        return all_issues
    else:
        print("✅ All charset tests passed!")
        return []

if __name__ == '__main__':
    issues = run_all_tests()
    if issues:
        sys.exit(1)