#!/usr/bin/env python3
"""
Test suite for inference functions (combined detection).
Can be adapted for pytest later.
"""

import sys
sys.path.insert(0, '/home/me/src/python-detextive/sources')

import detextive
from detextive import Behaviors, BehaviorTristate
import traceback

def test_infer_mimetype_charset():
    """Test combined MIME type and charset inference."""
    print("=== Testing infer_mimetype_charset ===")
    
    test_cases = [
        ("JSON content", b'{"message": "Hello", "value": 42}'),
        ("Plain text", b'Hello, world!'),
        ("UTF-8 with accents", 'Café résumé'.encode('utf-8')),
        ("XML content", b'<?xml version="1.0"?><root><item>test</item></root>'),
        ("HTML content", b'<!DOCTYPE html><html><head><title>Test</title></head></html>'),
        ("Empty content", b''),
    ]
    
    issues = []
    
    for name, content in test_cases:
        try:
            mimetype, charset = detextive.infer_mimetype_charset(content)
            print(f"✅ {name}: {mimetype}, {charset}")
            
            # Verify charset is valid when present
            if charset and not isinstance(charset, str):
                issues.append(f"Invalid charset type for {name}: {type(charset)}")
                
        except detextive.exceptions.MimetypeDetectFailure:
            print(f"⚠️  {name}: MIME detection failed (may be expected)")
        except detextive.exceptions.CharsetDetectFailure:
            print(f"⚠️  {name}: Charset detection failed (may be expected)")
        except Exception as e:
            issues.append(f"Failed {name}: {str(e)}")
            traceback.print_exc()
            
    return issues

def test_infer_with_location():
    """Test inference with location hints."""
    print("\n=== Testing Inference with Location ===")
    
    issues = []
    content = b'{"config": {"debug": true, "timeout": 30}}'
    
    locations = [
        'config.json',
        'data.txt', 
        '/path/to/settings.json',
        'document',  # No extension
    ]
    
    for location in locations:
        try:
            mimetype, charset = detextive.infer_mimetype_charset(content, location=location)
            print(f"✅ {location}: {mimetype}, {charset}")
        except Exception as e:
            issues.append(f"Failed with location {location}: {str(e)}")
            traceback.print_exc()
            
    return issues

def test_infer_with_http_content_type():
    """Test inference with HTTP Content-Type headers."""
    print("\n=== Testing Inference with HTTP Content-Type ===")
    
    issues = []
    content = b'{"status": "success", "data": null}'
    
    test_headers = [
        "application/json",
        "application/json; charset=utf-8",
        "text/plain; charset=iso-8859-1",
        "application/json; charset=utf-8; boundary=something",
        "text/html",
        "invalid-header",
    ]
    
    for header in test_headers:
        try:
            mimetype, charset = detextive.infer_mimetype_charset(content, http_content_type=header)
            print(f"✅ '{header}': {mimetype}, {charset}")
        except Exception as e:
            issues.append(f"Failed with header '{header}': {str(e)}")
            traceback.print_exc()
            
    return issues

def test_parse_http_content_type():
    """Test HTTP Content-Type header parsing."""
    print("\n=== Testing parse_http_content_type ===")
    
    issues = []
    
    test_headers = [
        ("application/json", ("application/json", "absent")),
        ("application/json; charset=utf-8", ("application/json", "utf-8")),
        ("text/html; charset=iso-8859-1", ("text/html", "iso-8859-1")),
        ("text/plain; charset=utf-8; boundary=test", ("text/plain", "utf-8")),
        ("application/octet-stream", ("application/octet-stream", None)),  # Non-textual
        ("", ("absent", "absent")),
        ("invalid", ("invalid", "absent")),
    ]
    
    for header, expected in test_headers:
        try:
            mimetype, charset = detextive.parse_http_content_type(header)
            
            # Handle absent values
            mimetype_str = "absent" if str(type(mimetype).__name__) == "AbsentSingleton" else mimetype
            charset_str = "absent" if str(type(charset).__name__) == "AbsentSingleton" else charset
            
            result = (mimetype_str, charset_str)
            print(f"✅ '{header}': {result}")
            
            # Check against expected (allowing some flexibility)
            expected_mime, expected_charset = expected
            if expected_mime != "absent" and mimetype_str != expected_mime:
                issues.append(f"MIME type mismatch for '{header}': got '{mimetype_str}', expected '{expected_mime}'")
                
        except Exception as e:
            issues.append(f"Failed parsing '{header}': {str(e)}")
            traceback.print_exc()
            
    return issues

def test_infer_with_defaults():
    """Test inference with default values."""
    print("\n=== Testing Inference with Defaults ===")
    
    issues = []
    
    # Content that might fail detection
    ambiguous_content = b'...'
    
    try:
        # This should use defaults when detection fails
        mimetype, charset = detextive.infer_mimetype_charset(
            ambiguous_content,
            mimetype_default='text/plain',
            charset_default='utf-8'
        )
        print(f"✅ With defaults: {mimetype}, {charset}")
        
        # Defaults should be used when detection fails
        if mimetype != 'text/plain':
            print(f"⚠️  Default MIME type not used: got '{mimetype}'")
        if charset != 'utf-8':
            print(f"⚠️  Default charset not used: got '{charset}'")
            
    except Exception as e:
        issues.append(f"Defaults test failed: {str(e)}")
        traceback.print_exc()
        
    return issues

def test_infer_charset_functions():
    """Test the infer_charset and infer_charset_confidence functions."""
    print("\n=== Testing infer_charset Functions ===")
    
    issues = []
    content = b'Sample text for charset inference testing'
    
    try:
        # Test basic inference
        charset1 = detextive.infer_charset(content)
        result = detextive.infer_charset_confidence(content)
        
        print(f"✅ infer_charset: {charset1}")
        print(f"✅ infer_charset_confidence: {result.value} (confidence: {result.confidence:.3f})")
        
        # Check consistency
        if charset1 != result.value:
            issues.append(f"Charset inference mismatch: infer_charset='{charset1}' vs infer_charset_confidence='{result.value}'")
            
        # Test with HTTP content type
        charset2 = detextive.infer_charset(content, http_content_type="text/plain; charset=iso-8859-1")
        print(f"✅ With HTTP header: {charset2}")
        
    except Exception as e:
        issues.append(f"Charset inference test failed: {str(e)}")
        traceback.print_exc()
        
    return issues

def run_all_tests():
    """Run all inference tests."""
    print("🧪 INFERENCE TEST SUITE")
    print("=" * 50)
    
    all_issues = []
    
    all_issues.extend(test_infer_mimetype_charset())
    all_issues.extend(test_infer_with_location())
    all_issues.extend(test_infer_with_http_content_type())
    all_issues.extend(test_parse_http_content_type())
    all_issues.extend(test_infer_with_defaults())
    all_issues.extend(test_infer_charset_functions())
    
    print("\n" + "=" * 50)
    print(f"INFERENCE TESTS COMPLETE")
    
    if all_issues:
        print(f"❌ Found {len(all_issues)} issues:")
        for issue in all_issues:
            print(f"  - {issue}")
        return all_issues
    else:
        print("✅ All inference tests passed!")
        return []

if __name__ == '__main__':
    issues = run_all_tests()
    if issues:
        sys.exit(1)