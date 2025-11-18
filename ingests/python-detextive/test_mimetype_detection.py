#!/usr/bin/env python3
"""
Test suite for MIME type detection functionality.
Can be adapted for pytest later.
"""

import sys
sys.path.insert(0, '/home/me/src/python-detextive/sources')

import detextive
from detextive import Behaviors
import traceback
from pathlib import Path

def test_basic_mimetype_detection():
    """Test basic MIME type detection with magic bytes."""
    print("=== Testing Basic MIME Type Detection ===")
    
    test_cases = [
        ("JSON", b'{"key": "value", "number": 42}'),
        ("PDF header", b'%PDF-1.4'),
        ("PNG header", b'\x89PNG\r\n\x1a\n'),
        ("JPEG header", b'\xff\xd8\xff'),
        ("ZIP header", b'PK\x03\x04'),
        ("XML", b'<?xml version="1.0"?><root></root>'),
        ("HTML", b'<!DOCTYPE html><html><body></body></html>'),
        ("Plain text", b'This is just plain text content'),
    ]
    
    issues = []
    
    for name, content in test_cases:
        try:
            mimetype = detextive.detect_mimetype(content)
            result = detextive.detect_mimetype_confidence(content)
            print(f"✅ {name}: {mimetype} (confidence: {result.confidence:.3f})")
            
            # Check consistency between functions
            if result.value != mimetype:
                issues.append(f"MIME type mismatch for {name}: detect_mimetype='{mimetype}' vs detect_mimetype_confidence='{result.value}'")
                
        except Exception as e:
            issues.append(f"Failed {name}: {str(e)}")
            print(f"❌ {name}: {str(e)}")
            traceback.print_exc()
            
    return issues

def test_mimetype_with_location():
    """Test MIME type detection using file extension fallback."""
    print("\n=== Testing MIME Type with Location ===")
    
    issues = []
    
    # Content without magic bytes that relies on extension
    plain_content = b'key: value\nother: data'
    
    test_locations = [
        ('file.json', 'application/json'),
        ('config.yaml', 'text/yaml'),
        ('script.py', 'text/x-python'),
        ('document.txt', 'text/plain'),
        ('page.html', 'text/html'),
        ('data.xml', 'text/xml'),
    ]
    
    for location, expected_type in test_locations:
        try:
            mimetype = detextive.detect_mimetype(plain_content, location=location)
            print(f"✅ {location}: {mimetype}")
            
            # Could be detected as expected type or text/plain
            if mimetype not in [expected_type, 'text/plain']:
                issues.append(f"Unexpected MIME type for {location}: got '{mimetype}', expected '{expected_type}' or 'text/plain'")
                
        except detextive.exceptions.MimetypeDetectFailure:
            print(f"⚠️  {location}: Detection failed (may be expected for ambiguous content)")
        except Exception as e:
            issues.append(f"Failed {location}: {str(e)}")
            traceback.print_exc()
            
    return issues

def test_mimetype_edge_cases():
    """Test MIME type detection edge cases."""
    print("\n=== Testing MIME Type Edge Cases ===")
    
    issues = []
    
    # Empty content
    try:
        mimetype = detextive.detect_mimetype(b'')
        print(f"✅ Empty content: {mimetype}")
    except detextive.exceptions.MimetypeDetectFailure:
        print("✅ Empty content: Detection failed (expected)")
    except Exception as e:
        issues.append(f"Empty content unexpected error: {str(e)}")
        
    # Very small content
    try:
        mimetype = detextive.detect_mimetype(b'x')
        print(f"✅ Single byte: {mimetype}")
    except detextive.exceptions.MimetypeDetectFailure:
        print("✅ Single byte: Detection failed (expected)")
    except Exception as e:
        issues.append(f"Single byte unexpected error: {str(e)}")
        
    # Binary content without clear magic bytes
    try:
        mimetype = detextive.detect_mimetype(b'\x01\x02\x03\x04\x05')
        print(f"✅ Random binary: {mimetype}")
    except detextive.exceptions.MimetypeDetectFailure:
        print("✅ Random binary: Detection failed (expected)")
    except Exception as e:
        issues.append(f"Random binary unexpected error: {str(e)}")
        
    return issues

def test_mimetype_with_charset_fallback():
    """Test MIME type detection when it falls back to charset-based detection."""
    print("\n=== Testing MIME Type with Charset Fallback ===")
    
    issues = []
    
    # Content that might not have magic bytes but should be detectable via charset
    text_content = b'Some plain text content without magic bytes'
    
    try:
        # This should either detect via magic or fall back to charset-based detection
        mimetype = detextive.detect_mimetype(text_content, charset='utf-8')
        print(f"✅ With charset hint: {mimetype}")
        
        # Without charset hint
        try:
            mimetype2 = detextive.detect_mimetype(text_content)
            print(f"✅ Without charset hint: {mimetype2}")
        except detextive.exceptions.MimetypeDetectFailure:
            print("✅ Without charset hint: Failed (may be expected)")
            
    except Exception as e:
        issues.append(f"Charset fallback test failed: {str(e)}")
        traceback.print_exc()
        
    return issues

def test_is_textual_mimetype():
    """Test the is_textual_mimetype utility function."""
    print("\n=== Testing is_textual_mimetype ===")
    
    issues = []
    
    textual_types = [
        'text/plain',
        'text/html',
        'application/json',
        'application/xml',
        'text/yaml',
        'application/javascript',
        'text/css',
    ]
    
    non_textual_types = [
        'image/jpeg',
        'image/png',
        'video/mp4',
        'audio/mpeg',
        'application/pdf',
        'application/octet-stream',
        'application/zip',
    ]
    
    try:
        for mimetype in textual_types:
            is_textual = detextive.is_textual_mimetype(mimetype)
            if not is_textual:
                issues.append(f"'{mimetype}' should be textual but returned False")
            print(f"✅ {mimetype}: textual = {is_textual}")
            
        for mimetype in non_textual_types:
            is_textual = detextive.is_textual_mimetype(mimetype)
            if is_textual:
                issues.append(f"'{mimetype}' should not be textual but returned True")
            print(f"✅ {mimetype}: textual = {is_textual}")
            
    except Exception as e:
        issues.append(f"is_textual_mimetype test failed: {str(e)}")
        traceback.print_exc()
        
    return issues

def run_all_tests():
    """Run all MIME type detection tests."""
    print("🧪 MIME TYPE DETECTION TEST SUITE")
    print("=" * 50)
    
    all_issues = []
    
    all_issues.extend(test_basic_mimetype_detection())
    all_issues.extend(test_mimetype_with_location())
    all_issues.extend(test_mimetype_edge_cases())
    all_issues.extend(test_mimetype_with_charset_fallback())
    all_issues.extend(test_is_textual_mimetype())
    
    print("\n" + "=" * 50)
    print(f"MIME TYPE TESTS COMPLETE")
    
    if all_issues:
        print(f"❌ Found {len(all_issues)} issues:")
        for issue in all_issues:
            print(f"  - {issue}")
        return all_issues
    else:
        print("✅ All MIME type tests passed!")
        return []

if __name__ == '__main__':
    issues = run_all_tests()
    if issues:
        sys.exit(1)